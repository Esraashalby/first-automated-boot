from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database

cluster = MongoClient("mongodb+srv://esraa:esraa1@cluster0.f084i.mongodb.net/store?retryWrites=true&w=majority")
db = cluster["store"]
users = db["users"]
orders = db["order"]
product = db["product"]
app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    txt = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")
    res = MessagingResponse()
    user = users.find_one({"number": number})
    # main page
    if bool(user) == False:
        users.insert_one({"number": number, "status": "main", "messages": []})
        res.message(
            "اهلا بك في متجرنا📷 \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
        return str(res)
    elif user["status"] == "main":
        try:
            users.update_one({"number": number}, {"$push": {"messages": {"text": txt, "date": datetime.now()}}})
            option = int(txt)
        except:
            res.message("اختيار خاطيء!")
            return str(res)
        if option == 1:
            persistent_action = ['geo:37.787890,-122.391664|375 Beale St']

            res.message("اتصل بنا على: 0120123578888 \n \n \n  📍 العنوان: 5 شارع النصر - المنشية")
            return str(res)
        elif option == 2:
            users.update_one({"number": number}, {"$set": {"status": "order"}})
            res.message("لتأجير الكاميرات 1️⃣ \n \n لتأجير العدسات 2️⃣ \n \n للرجوع للقائمة الرئيسية 0️⃣")
            return str(res)
        elif option == 3:
            order = db["order"]
            products = list(order.find({"number": number}))
            status = list(order.find({"number": number}))[0]
            test= status['order_status']
            res.message(f"{len(products)}")
            res.message(f"{test}")
            return str(res)
        elif option == 4:
            res.message("مواعيد العمل في المتجر من الساعة 8ص إلى 9م \n \n تسعدنا زيارتك 💥❤")
            return str(res)
        else:
            return str(res)

        users.update_one({"number": number}, {"$push": {"messages": {"text": txt, "date": datetime.now()}}})
        return str(res)
    #menu page 1
    elif user["status"] == "order":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif option == 1:
            users.update_one({"number": number}, {"$set": {"status": "rentcamera"}})
            res.message("كاميرات: \n \n 1️⃣ نيكون \n \n 2️⃣ كانون \n \n 3️⃣ سيجما")
            return str(res)
        elif option == 2:
            users.update_one({"number": number}, {"$set": {"status": "rentlense"}})
            res.message("عدسات: \n \n 1️⃣ نيكون \n \n 2️⃣ كانون \n \n 3️⃣ سيجما")
            return str(res)
        elif 10 <= option <= 20:
            camera = ["canon", "nikon", "sigma"]
            select = camera[option - 1]
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": select}})
            res.message("Excelent choice 🥳 \n please enter your address")
            return str(res)
        else:
            res.message("اختيار خاطيء..!")
            return str(res)
    #تاأجير الكاميرات
    elif user["status"] == "rentcamera":
        try:
            option = int(txt)
        except:
            res.message("اختيار خاطئ.!")
            return str(res)
        if option == 1:
            users.update_one({"number": number}, {"$set": {"status": "rent_nikon_camera"}})
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['nikon'])
            i = -1
            for x in range(len(canon_cameras)):
                i = i + 1
                for pic in canon_cameras[i]['pictures']:
                    msg = res.message(canon_cameras[i]['name'])
                    msg.media(pic)
            return str(res)
        elif option == 2:
            users.update_one({"number": number}, {"$set": {"status": "rent_canon_camera"}})
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['canon'])
            i = -1
            for x in range(len(canon_cameras)):
                i = i + 1
                for pic in canon_cameras[i]['pictures']:
                    msg = res.message(canon_cameras[i]['name'])
                    msg.media(pic)
            return str(res)
        elif option == 3:
            users.update_one({"number": number}, {"$set": {"status": "rent_sigma_camera"}})
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['sigma'])
            i = -1
            for x in range(len(canon_cameras)):
                i = i + 1
                for pic in canon_cameras[i]['pictures']:
                    msg = res.message(canon_cameras[i]['name'])
                    msg.media(pic)
            return str(res)
        else:
            res.message("اختيار خاطيء..!")
            return str(res)
    #تأجير العدسات
    elif user["status"] == "rentlense":
        try:
            option = int(txt)
        except:
            res.message("اختيار خاطئ.!")
            return str(res)
        if option == 1:
            users.update_one({"number": number}, {"$set": {"status": "rent_nikon_lens"}})
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['lenses']['nikon'])
            i = -1
            for x in range(len(canon_cameras)):
                i = i + 1
                for pic in canon_cameras[i]['pictures']:
                    msg = res.message(canon_cameras[i]['name'])
                    msg.media(pic)
            return str(res)
        elif option == 2:
            users.update_one({"number": number}, {"$set": {"status": "rent_canon_lens"}})
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['lenses']['canon'])
            i = -1
            for x in range(len(canon_cameras)):
                i = i + 1
                for pic in canon_cameras[i]['pictures']:
                    msg = res.message(canon_cameras[i]['name'])
                    msg.media(pic)
            return str(res)
        elif option == 3:
            users.update_one({"number": number}, {"$set": {"status": "rent_sigma_lens"}})
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['lenses']['sigma'])
            i = -1
            for x in range(len(canon_cameras)):
                i = i + 1
                for pic in canon_cameras[i]['pictures']:
                    msg = res.message(canon_cameras[i]['name'])
                    msg.media(pic)
            return str(res)
        else:
            res.message("اختيار خاطيء..!")
            return str(res)
    #تأكيد الطلب
    elif user["status"]=="rent_nikon_camera":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['nikon'])
            camera_selected = canon_cameras[option-1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)
    elif user["status"] == "rent_canon_camera":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['canon'])
            camera_selected = canon_cameras[option - 1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)
    elif user["status"] == "rent_sigma_camera":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['sigma'])
            camera_selected = canon_cameras[option - 1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)
    elif user["status"] == "rent_s":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['sigma'])
            camera_selected = canon_cameras[option - 1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)
    elif user["status"] == "rent_sigma_camera":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['cameras']['sigma'])
            camera_selected = canon_cameras[option - 1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)
    elif user["status"] == "rent_nikon_lens":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['lenses']['nikon'])
            camera_selected = canon_cameras[option - 1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)

    elif user["status"] == "rent_canon_lens":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['lenses']['canon'])
            camera_selected = canon_cameras[option - 1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)

    elif user["status"] == "rent_sigma_lens":
        try:
            option = int(txt)
        except:
            res.message("please enter a valid choice!")
            return str(res)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            res.message(
                "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
            return str(res)
        elif 1 <= option <= 3:
            links = db["products"]
            products = list(links.find())[0]
            canon_cameras = (products['rent']['lenses']['sigma'])
            camera_selected = canon_cameras[option - 1]['name']
            users.update_one({"number": number}, {"$set": {"status": "address"}})
            users.update_one({"number": number}, {"$set": {"item": camera_selected}})
            res.message("اختيار رائع 🤩 \n من فضلك ادخل العنوان...")
            return str(res)
        else:
            res.message("اختيار خاطئ")
            return str(res)



    elif user["status"] == "address":
        select = user["item"]
        res.message(f"نشكرك على التسوق معنا 🤍 \n طلبك {select} تم استلامه وسيتم توصيله إلى {txt} خلال 24 ساعة ")
        users.update_one({"number": number}, {"$push": {"messages": {"text": txt, "date": datetime.now()}}})
        orders.insert_one({"number": number,"order_status":"recieved", "item": select, "address": txt, "order_time": datetime.now()})
        users.update_one({"number": number}, {"$set": {"status": "ordered"}})
        return str(res)
    elif user["status"] == "ordered":
        users.update_one({"number": number}, {"$set": {"status": "main"}})
        res.message(
            "اهلا بك مرة ثانية.... \n للاتصال بنا ارسل 1️⃣  \n  لعمل طلب ارسل 2️⃣ \n لمشاهدة عدد الطلبات المرتبط بحسابك ارسل 3️⃣ \n لمعرفة مواعيد العمل ارسل 4️⃣")
        return str(res)


if __name__ == "__main__":
    app.run()
