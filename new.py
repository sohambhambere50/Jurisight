import smtplib

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("sohambhambere55@gmail.com", "lxjeokzbxrleefcf")
print(" Login successful")
