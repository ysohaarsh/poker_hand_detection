from ultralytics import YOLO
import cv2
import cvzone
import math
import argparse
import PokerHandFunction

classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS']


def parse_args():
    parser = argparse.ArgumentParser(description="Detect playing cards and name the poker hand.")
    parser.add_argument("--source", default="0",
                        help="webcam index (default 0) or path to a video file")
    parser.add_argument("--model", default="playingCards.pt", help="path to the YOLO weights")
    parser.add_argument("--conf", type=float, default=0.5, help="minimum detection confidence")
    return parser.parse_args()


def main():
    args = parse_args()
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)
    cap.set(3, 1280)
    cap.set(4, 720)
    model = YOLO(args.model)

    while True:
        success, img = cap.read()
        if not success:  # camera unavailable or end of video
            break
        results = model(img, stream=True)
        hand = []
        for r in results:
            for box in r.boxes:
                # Bounding Box
                x1, y1, x2, y2 = (int(v) for v in box.xyxy[0])
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))
                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])

                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)),
                                   scale=1, thickness=1)

                if conf > args.conf:
                    hand.append(classNames[cls])

        hand = list(set(hand))
        if len(hand) == 5:
            result = PokerHandFunction.findPokerHand(hand)
            cvzone.putTextRect(img, f'Your Hand: {result}', (300, 75), scale=3, thickness=5)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
