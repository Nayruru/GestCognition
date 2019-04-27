'''
ჯგუფის ნომერი: 4
პროექტის თემა: Hand Gesture Recognition using Python and OpenCV
ჯგუფის წევრები: ელენე კვარაცხელია, ანრი გიორგანაშვილი, ანა ონიანაშვილი, ანა ბერიშვილი

'''

import cv2  # გამოსახულების მისაღებად
import numpy as np

#   ვააქტიურებთ კამერას
capture = cv2.VideoCapture(0) # 0 არის კამერის იდენტიფიკატორი (თუ მეორე კამერაც გვაქვს 1-ანს ჩავწერთ)

# isOpened აბრუნებს Boolean-ს (გააქტიურებულია თუ არა კამერა)
while capture.isOpened():

    # თუ შემდეგი Frame არსებობს ret იქნება True (და არაფერში არ ვიყენებთ, უბრალოდ 2 პარამეტრს აბრუნებს read())
    # frame კი კადრია
    ret, frame = capture.read()

    #   ეკრანზე გამოსახულების რაღაც ნაწილში უნდა მივუთითოთ ადგილი სადაც ხელი უნდა შევიტანოთ
    #   კოორდ1, კოორდ2 მოპირისპირე კუთხეებია
    #   fraction - კოორდინატში შეყვანილ რიცხვში მძიმის მერე სიზუსტე (ჩვენ არ გვაქვს ათწილადი ამიტომ 0-ს ვწერთ)
    #                     კოორდ 1    კოორდ 2  ფერი (R,G,B) # fraction
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)

    #   მიღებული კადრიდან ვჭრით მხოლოდ იმ ადგილს სადაც ხელი ფიქსირდება
    crop_image = frame[100:300, 100:300]
    
    #   ვაბუნდოვნებთ კადრს, რომ მარტივი დასამუშავებელი იყოს
    #                         source     x, y გაბუნდოვნების კოეფიციენტები
    blur = cv2.GaussianBlur(crop_image, (3, 3), 0)  # 0 - BorderType

    #   BLUE-GREEN-RED -> HUE-SATURATION-VALUE  Colorspace Convertion
    #   BGR/RGB ფერების მოდელთან შედარებით HSV-ში ფერების Range-ის განსაზღვრა უფრო მარტივია
    #   ამიტომ იყენებს OpenCV HSV-მოდელს კადრებში ობიექტების აღსაქმელად
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #   ვქმნით მასკას (ანუ ვათეთრებთ იმ ობიექტს რომელიც გვჭირდება და დანარჩენს ვაშავებთ)
    #   ვუთითებთ კანის ფერის Range-ს   საწყისი  colorizer.org   საბოლოო
    mask2 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))

    #   კერნელის ინიციალიზაცია მორფოლოგიური ტრანსფორმაციისთვის
    #   შეამჩნევდით რომ ვიყენებთ numpy-ს (np) რითიც ვქმნით 5x5 მატრიცას სადაც ყველა წევრი არის 1
    #   ჯერ ვერ გავიგე 5x5 1-იანებით გავსებული კერნელი რას აკეთებს მაგრამ 3x3 100%-ით აბუნდოვნებს
    kernel = np.ones((5, 5))

    #   მასკის შექმნისას (მე-40 ხაზი) რა თქმა უნდა ხელის გარდა ფონზე სხვა რაღაცეებიც შეიძლება გათეთრდეს
    #   იმიტომ რომ კანის ფერის range-ში სხვა ობიექტების ფერიც შეიძლება იყოს
    #   ანუ გამოსახულებაში გვექნება "ხმაური" ( background noise )
    #   იმისთვის რომ მოვიშოროთ ეს "ხმაური" 
    #   მორფოლოგიური ტრანსფორმაცია გვჭირდება
    #   გვაქვს მრავალი მორფ.ტრანსფორმაცია მაგ: ეროზია(გამოსახულებას გარედან ჭამს), Opening და სხვა
    #   https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
    #               ყველა გამოსახულებას გაასქელებს
    dilation = cv2.dilate(mask2, kernel, iterations=1)
    #              და ეროზიისას ზედმეტი წერტილები დაიკარგება
    erosion = cv2.erode(dilation, kernel, iterations=1)