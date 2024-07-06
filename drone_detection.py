from ultralytics import YOLO
from geopy.geocoders import Nominatim
import cv2
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#./static/files/1.jpg
cap=cv2.VideoCapture(0)

frame_width=int(cap.get(3))
frame_height = int(cap.get(4))

out=cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))

flag=True
def send_email(loc,long,lat):
    try:
        sender_email = 'vekariyakevin4@gmail.com'
        receiver_email = 'kevinvekariya274@gmail.com'
        subject = "Test Email"
        message = f"Drone has been Decetcted at {long} {lat} {loc}"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Replace with the appropriate port for your SMTP server
        smtp_username = "your_smtp_username"  # If authentication is required
        smtp_password = 'jqtewvcwqehzbpep'  # If authentication is required
        # Create a message container
        msg = MIMEMultipart()
        msg['From'] = 'vekariyakevin4@gmail.com'
        msg['To'] = 'kevinvekariya274@gmail.com'
        msg['Subject'] = 'Drone dectected'

        # Attach the message to the email
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # If using TLS
        server.login(sender_email, smtp_password)  # Uncomment if authentication is required

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the connection
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


model=YOLO("model/best.pt")
classNames = ["Drone"]
while True:
    success, img = cap.read()

    results=model(img,stream=True)

    for r in results:
        boxes=r.boxes
        for box in boxes:
            x1,y1,x2,y2=box.xyxy[0]
            #print(x1, y1, x2, y2)
            x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
            print(x1,y1,x2,y2)
            cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
            #print(box.conf[0])
            conf=math.ceil((box.conf[0]*100))/100
            cls=int(box.cls[0])
            class_name=classNames[cls]
            label=f'{class_name}{conf}'
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            #print(t_size)
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
            cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
            geolocator = Nominatim(user_agent="geoapiExercises")

            # Assign Latitude & Longitude
            Latitude = "22.2887007"
            Longitude = "73.3585495"

            # Displaying Latitude and Longitude
            print("Latitude: ", Latitude)
            print("Longitude: ", Longitude)

            # Get location with geocode
            location = geolocator.geocode(Latitude+","+Longitude)

            # Display location
            print("\nLocation of the given Latitude and Longitude:")
            print(location)
            if flag==True:
                send_email(location,Latitude,Longitude)
                flag=False

    out.write(img)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
out.release()
