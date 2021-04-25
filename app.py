from flask import Flask, render_template, request, redirect, send_file
import os
from flask_restful import Api
import numpy as np
import cv2

app = Flask(__name__)
api = Api(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
imSavePath = "./"


def processImage():
    # zaladowanie obrzu do przetwarzania
    image2process = cv2.imread(os.path.join(imSavePath, "image.png"))

    # kreska bialo-czerwona
    p = np.array([(255, 255, 255), (255, 255, 255), (255, 255, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255)])
    # kreska czerwono-biala
    l = np.array([(0, 0, 255), (0, 0, 255), (0, 0, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)])

    # iteracja poszukujaca poziomo
    for i in range(len(image2process)):
        for k in [image2process[i][j:j + len(p)] for j in range(len(image2process[i]) - len(p) + 1)]:
            if np.array_equal(k, p):
                image2process = cv2.rotate(image2process, cv2.cv2.ROTATE_90_CLOCKWISE)
                cv2.imwrite(os.path.join(imSavePath, "imageProcessed.png"), image2process)
                return 1  # zwraca 1 kiedy wykryto linie pozioma bialo-czerwona (obrot -90)

            elif np.array_equal(k, l):
                image2process = cv2.rotate(image2process, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
                cv2.imwrite(os.path.join(imSavePath, "imageProcessed.png"), image2process)
                return -1  # zwraca -1 kiedy wykryto linie pozioma czerwono-biala (obrot 90)

    # iteracja poszukujaca pionowo
    for i in range(len(image2process[0])):
        for j in range(len(image2process) - len(p) + 1):
            ar = [image2process[j][i], image2process[j + 1][i], image2process[j + 2][i], image2process[j + 3][i],
                  image2process[j + 4][i], image2process[j + 5][i]]
            if np.array_equal(ar, p):

                cv2.imwrite(os.path.join(imSavePath, "imageProcessed.png"), image2process)
                return 2  # zwraca 2 kiedy wykryta linia pionowa jest bialo-czerwona (brak obrotu)

            elif np.array_equal(ar, l):

                image2process = cv2.rotate(image2process, cv2.cv2.ROTATE_180)
                cv2.imwrite(os.path.join(imSavePath, "imageProcessed.png"), image2process)
                return -2  # zwraca -2 kiedy wykryta linia pionowa jest czerwono-biala (obrot o 180)

    return 0  # zwraca 0 kiedy nie znaleziono dopasowania


@app.route('/rotate', methods=["POST", "GET"])
def rotate():
    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            image.save(os.path.join(imSavePath, "image.png"))

            temp = processImage()

            # wartosci rozne od 0 uznajemy za prawidlowe i zwracamy obrobiony obraz
            if temp != 0:

                return send_file(os.path.join(imSavePath, "imageProcessed.png")), 200

            elif temp == 0:
                # no content

                return ('', 204)
            return redirect(request.url)

    return render_template("public/upload_image.html")


if __name__ == '__main__':
    app.run()  # run our app
