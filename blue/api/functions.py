import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
angleListS1 = []
angleListS2 = []
comparedAngles = []
comparedFeatures = []


def pose_detection(sources):

    for x in range(0, len(sources)):
        frames_counter = 0
        cap = cv2.VideoCapture(sources[x])

        # Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
            while cap.isOpened():
                frames_counter += 1
                ret, frame = cap.read()

                # Recolor image to RGB
                try:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                except Exception as e:
                    print(e)

                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    landmark_checker(landmarks, x)

                except Exception as e:
                    print(e)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

                # cv2.imshow('Mediapipe Feed', image)
                if cv2.waitKey(1) & frames_counter == 128:
                    break
            cap.release()
            cv2.destroyAllWindows()
    match = compare_angels(angleListS1, angleListS2)
    angleListS1.clear()
    angleListS2.clear()
    comparedAngles.clear()
    comparedFeatures.clear()

    return match


def landmark_checker(landmarks, x):
    threshold = 0.90
    angles_dictionary = {
        "LEFT_ELBOW": -1,
        "RIGHT_ELBOW": -1,
        "RIGHT_SHOULDER": -1,
        "LEFT_SHOULDER": -1,
        "LEFT_HIP": -1,
        "RIGHT_HIP": -1,
        "LEFT_KNEE": -1,
        "RIGHT_KNEE": -1,
    }

    # Angle for Left ELBOW
    if landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        end = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)

        angles_dictionary['LEFT_ELBOW'] = angle

    # Angle for RIGHT ELBOW
    if landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        end = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)
        angles_dictionary['RIGHT_ELBOW'] = angle

    # angle for RIGHT SHOULDER
    if landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        end = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)
        angles_dictionary['RIGHT_SHOULDER'] = angle

    # angle for LEFT SHOULDER
    if landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        end = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)
        angles_dictionary['LEFT_SHOULDER'] = angle

    # angle for RIGHT KNEE
    if landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        end = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)

        angles_dictionary['RIGHT_KNEE'] = angle

    # angle for LEFT KNEE
    if landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        end = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)

        angles_dictionary['LEFT_KNEE'] = angle

    # angle for left HIP
    if landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        end = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)
        angles_dictionary['LEFT_HIP'] = angle

    # angle for right HIP
    if landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility > threshold and \
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].visibility > threshold:
        first = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        mid = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        end = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
               landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        angle = calculate_angle(a=first, b=mid, c=end)

        angles_dictionary['RIGHT_HIP'] = angle

    if x == 0:
        angleListS1.append(angles_dictionary)
    if x == 1:
        angleListS2.append(angles_dictionary)


def compare_angels(angleListS1, angleListS2):
    features = ['LEFT_ELBOW', 'RIGHT_ELBOW', 'RIGHT_SHOULDER', 'LEFT_SHOULDER', 'LEFT_HIP', \
                'RIGHT_HIP', 'LEFT_KNEE', 'RIGHT_KNEE']
    subtractedAngles = []

    for listIndex in range(0, 128):
        for ValueIndex in range(0, len(features)):
            if (list(angleListS1[listIndex].values())[ValueIndex] > -1) and (
                    list(angleListS2[listIndex].values())[ValueIndex] > -1):
                subtractedValue = list(angleListS1[listIndex].values())[ValueIndex] - \
                                  list(angleListS2[listIndex].values())[ValueIndex]
                subtractedAngles.append(abs(round(subtractedValue, 2)))
            else:
                features[ValueIndex] = "NO FEATURE FOUND"
        comparedAngles.append(subtractedAngles)
        subtractedAngles = []
        comparedFeatures.append(features)
    match = analysis(comparedAngles)
    return match


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    return abs(round(radians, 2))


def analysis(subtractedAngles):
    listOfRatings = []
    for frame in subtractedAngles:
        feature_found = 0
        for feature in frame:
            if feature > 0.5:
                feature_found += 1
        if len(frame) > 0:
            rating = (feature_found / len(frame))
            listOfRatings.append(rating)

    rating_Count = 0
    for rating in listOfRatings:
        if rating < 0.5:
            rating_Count += 1

    match = rating_Count / len(listOfRatings) * 100
    return match