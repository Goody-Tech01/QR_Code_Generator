import qrcode
import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox,filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


root=ctk.CTk()
root.title("QR Code Generator")
root.geometry("900x480")
root.resizable(True,True)
generated_image = None

def generate_code():
    data = entry.get()

    if not data:
        messagebox.showwarning( "Input Error","Please enter data")
        return

    selected = options.get()


    if selected == "Website(URL)":
        if not data.startswith(("http://", "https://")):
            messagebox.showwarning("Invalid URL","URL must start with http:// or https://" )
            return


    elif selected == "Email":
        if "@" not in data or "." not in data:
            messagebox.showwarning("Invalid Email","Please enter a valid email")
            return

        data = f"mailto:{data}"


    elif selected == "Phone Number":
        if not data.isdigit():
            messagebox.showwarning("Invalid Phone Number","Phone number must contain only digits")
            return

        data = f"tel:{data}"


    elif selected == "SMS Message":
        data = f"SMStO:{data}"



    elif selected == "Wi-Fi Connection":

        if not data:
            messagebox.showwarning("Input Error", "Please enter Wi-Fi name")
            return

        data = f"WIFI:T:WPA;S:{data};;"


    elif selected == "Location (Google Maps)":
        data = f"https://maps.google.com/?q={data}"



    elif selected == "Contact (vCard)":

        try:
            full_name, phone, email = data.split(",")
            data = f"""BEGIN:VCARD
VERSION:3.0
FN:{full_name}          
TEL:{phone}
EMAIL:{email}  
END:VCARD
"""
        except ValueError:
            messagebox.showwarning( "Input Error","Enter data as:\nName,Phone,Email")
            return


    fill_color = fill_entry.get() or "black"
    back_color = back_entry.get() or "white"

    level_map = { "High(H)": qrcode.constants.ERROR_CORRECT_H,"Medium(M)": qrcode.constants.ERROR_CORRECT_M,
        "Low(L)": qrcode.constants.ERROR_CORRECT_L}

    qr = qrcode.QRCode(version=1, error_correction=level_map[level.get()], box_size=8,border=2,)

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    global generated_image
    generated_image = img

    display_image(img)

    status_label.configure(text="QR Code Generated Successfully",text_color="lightgreen")

def download_code():
   if generated_image is None:
       status_label.configure(text="Generate a QR code first",text_color="red")
       return

   file_path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png")],
                         title="Save QR Code")
   if file_path:
       generated_image.save(file_path)
       status_label.configure(text="QR Code saved successfully",text_color="lightgreen")


def display_image(img):
   img = img.resize((200, 200))
   ctk_img = CTkImage(light_image=img,dark_image=img,size=(200, 200))

   panel.configure(image=ctk_img, text="")
   panel.image = ctk_img


frame=CTkFrame(root,fg_color="black",height=470,width=850)
frame.place(relx=0.5,rely=0.5,anchor="center")

CTkLabel(frame,text="QR Code Generator",text_color="white",font=("Seguo UI",28,"normal")).place(x=350,y=10)
(CTkLabel(frame,text="Create QR codes instantly and save them for free.",text_color="white",font=("Arial",15))
 .place(x=323,y=40))


qr=CTkFrame(frame,fg_color="#8B5CF6",height=340,width=390,corner_radius=15)
qr.place(x=18,y=80)
qr2=CTkFrame(frame,fg_color="#F5F5F5",height=340,width=390,corner_radius=15)
qr2.place(x=440,y=80)


CTkLabel(qr,text="Select QR Code Type:",text_color="white",font=("Seguo UI",18,"normal")).place(x=10,y=10)
options = ctk.CTkComboBox(qr,values=["Website(URL)", "Phone Number", "Email", "SMS Message","Wi-Fi Connection",
                                     "Contact (vCard)","Location (Google Maps)",],state="readonly",width=250,
                                      fg_color="#1F2937",button_color="#7C3AED",dropdown_fg_color="#111827",
                                      dropdown_hover_color="#374151")
options.set("Website(URL)")
options.place(x=10, y=40)
entry=ctk.CTkEntry(qr,placeholder_text="Enter your data",width=350,fg_color="#1F2937")
entry.place(x=10,y=70)


CTkLabel(qr,text="Error Correction Level",text_color="white",font=("Seguo UI",18,"normal")).place(x=10,y=105)
level=ctk.CTkComboBox(qr,values=["High(H)", "Medium(M)", "Low(L)"],state="readonly",width=250,fg_color="#1F2937",
                      dropdown_fg_color="#111827",button_color="#7C3AED",dropdown_hover_color="#374151")
level.set("Medium(M)")
level.place(x=10,y=135)


CTkLabel(qr,text="Fill Color",text_color="white",font=("Seguo UI",18,"normal")).place(x=10,y=170)
fill_entry=ctk.CTkEntry(qr,placeholder_text="e.g blue",width=350,fg_color="#1F2937")
fill_entry.place(x=10,y=200)


CTkLabel(qr,text="Background Color",text_color="white",font=("Seguo UI",18,"normal")).place(x=10,y=235)
back_entry=ctk.CTkEntry(qr,placeholder_text="e.g red",width=350,fg_color="#1F2937")
back_entry.place(x=10,y=265)


gen_code = CTkButton(qr,text="Generate QR Code",width=200,height=40,corner_radius=10,
                     fg_color="#1F2937",hover_color="#7C3AED",command=generate_code)
gen_code.place(relx=0.5, rely=0.93, anchor="center")


CTkLabel(qr2,text="QR Code Preview",text_color="black",font=("Seguo UI",18,"normal")).place(x=10,y=10)


down_code = CTkButton(qr2,text="Download QR Code",width=200,height=40,corner_radius=10,
                     fg_color="#1F2937",hover_color="#7C3AED",command=download_code)
down_code.place(relx=0.5, rely=0.93, anchor="center")


panel_frame = CTkFrame(qr2,fg_color="#FAFAFA",width=250,height=250,corner_radius=15)
panel_frame.place(x=70, y=40)
panel_frame.pack_propagate(False)
panel = CTkLabel(panel_frame, text="")
panel.pack(expand=True)

status_label = CTkLabel(frame,text="",text_color="lightgreen",font=("Arial", 14))
status_label.place(relx=0.5, y=450, anchor="center")

root.mainloop()