import tkinter as tk
from tkinter import messagebox
from otp_generator import OTPGenerator

class OTPAuthenticator:
    def __init__(self, master):
        self.master = master
        master.title("OTP Authenticator")

        self.otp_gen = OTPGenerator(port_name='COM7')
        self.current_otp = None
        self.target_phone_number = None

        self.label = tk.Label(master, text="Enter phone number:")
        self.label.pack()

        self.phone_entry = tk.Entry(master)
        self.phone_entry.pack()

        self.send_otp_button = tk.Button(master, text="Send OTP", command=self.send_otp)
        self.send_otp_button.pack()

        self.resend_otp_button = tk.Button(master, text="Resend OTP", command=self.resend_otp)
        self.resend_otp_button.pack()

        self.otp_label = tk.Label(master, text="Enter OTP:")
        self.otp_label.pack()

        self.otp_entry = tk.Entry(master)
        self.otp_entry.pack()

        self.auth_button = tk.Button(master, text="Authenticate", command=self.authenticate)
        self.auth_button.pack()

    def send_otp(self):
        self.target_phone_number = self.phone_entry.get()
        if not self.target_phone_number:
            messagebox.showerror("Error", "Phone number cannot be empty.")
            return
        self.current_otp = self.otp_gen.generate_otp()
        if self.otp_gen.send_sms(self.target_phone_number, f"Your OTP is: {self.current_otp}"):
            messagebox.showinfo("Info", "OTP sent successfully!")
        else:
            messagebox.showerror("Error", "Failed to send OTP. Check your connection.")

    def resend_otp(self):
        if not self.target_phone_number:
            messagebox.showerror("Error", "Please enter a phone number first.")
            return
        self.current_otp = self.otp_gen.generate_otp()
        if self.otp_gen.send_sms(self.target_phone_number, f"Your new OTP is: {self.current_otp}"):
            messagebox.showinfo("Info", "OTP resent successfully!")
        else:
            messagebox.showerror("Error", "Failed to resend OTP. Check your connection.")

    def authenticate(self):
        entered_otp = self.otp_entry.get()
        if entered_otp == self.current_otp:
            messagebox.showinfo("Success", "OTP authenticated successfully!")
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")

if __name__ == "__main__":
    root = tk.Tk()
    otp_authenticator = OTPAuthenticator(root)
    root.mainloop()
