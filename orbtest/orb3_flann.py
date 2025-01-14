import numpy as np
import cv2.cv2 as cv2

def orb3_flann():
    # Read the query image as query_img
    # and train image This query image
    # is what you need to find in train image
    # Save it in the same directory
    # with the name image.jpg
    img1 = cv2.imread('score_overlay_2022.png')
    img2 = cv2.imread('2022/frame1992.png')
    assert img1 is not None
    assert img2 is not None

    # img2 = cv2.resize(img2, (1280, 720))

    # Convert it to grayscale
    # query_img_bw = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # train_img_bw = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Initialize the ORB detector algorithm
    orb = cv2.ORB_create()

    # Now detect the keypoints and compute
    # the descriptors for the query image
    # and train image
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    FLANN_INDEX_LSH = 6
    index_params = dict(
        algorithm=FLANN_INDEX_LSH,
        table_number=6,
        key_size=12,
        multi_probe_level=1
    )
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    t = cv2.estimateAffinePartial2D(src_pts, dst_pts)

    transform = {
        'scale': t[0][0, 0],
        'tx': t[0][0, 2],
        'ty': t[0][1, 2],
    }
    TEMPLATE_SCALE = 1

    def transformPoint(point):
        # Transforms a point from template coordinates to image coordinates
        scale = transform['scale'] * TEMPLATE_SCALE
        tx = transform['tx']
        ty = transform['ty']
        return np.int32(np.round(point[0] * scale + tx)), np.int32(np.round(point[1] * scale + ty))

    def _cornersToBox(tl, br):
        return np.array([
            [tl[0], tl[1]],
            [br[0], tl[1]],
            [br[0], br[1]],
            [tl[0], br[1]]
        ])

    def _drawBox(img, box, color):
        cv2.polylines(img, [box], True, color, 2, cv2.LINE_AA)

    box = _cornersToBox(transformPoint((0, 0)), transformPoint((1280, 170)))
    _drawBox(img2, box, (255, 255, 0))

    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, [[m] for m in good], None,
                              flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    scale_factor = .5
    img3 = cv2.resize(img3, (
        np.int32(1280*2/2),
        np.int32(720/2)
    ))
    cv2.imshow("Matches", img3)
    cv2.waitKey()


if __name__ == "__main__":
    orb3_flann()
