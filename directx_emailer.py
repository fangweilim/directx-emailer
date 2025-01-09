import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import tkinter as tk
from tkinter import messagebox, ttk
import keyring
import logging

# Enable logging for debugging
logging.basicConfig(filename='emailer.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def collect_directx_info(output_file='dxdiag_report.txt'):
    """
    Collects DirectX system information using dxdiag command and saves it to a text file.
    """
    try:
        subprocess.run(['dxdiag', '/t', output_file], check=True)
        logging.info(f"DirectX information saved to {output_file}")
        return output_file
    except FileNotFoundError:
        logging.error("dxdiag command not found.")
        messagebox.showerror("Error", "dxdiag command not found. Ensure DirectX is installed.")
        raise
    except subprocess.CalledProcessError as e:
        logging.error(f"dxdiag command failed: {e}")
        messagebox.showerror("Error", f"An error occurred while running dxdiag: {e}")
        raise

def create_email(sender_email, receiver_email, subject, body, attachment_path):
    """
    Creates an email with the specified details and attachment.
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)
    except FileNotFoundError:
        logging.error(f"Attachment file not found: {attachment_path}")
        messagebox.showerror("Error", f"Attachment file not found: {attachment_path}")
        raise
    return msg

def send_email(msg, sender_email, password):
    """
    Sends the email using the provided credentials.
    """
    try:
        with smtplib.SMTP('smtp.mail.me.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            logging.info("Email sent successfully!")
            messagebox.showinfo("Success", "Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed. Check your email and app-specific password.")
        messagebox.showerror("Error", "Authentication failed. Check your email and app-specific password.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")
        raise


def save_credentials():
    """
    Save sender email and password securely using keyring.
    """
    try:
        keyring.set_password("DirectX_Emailer", sender_email.get(), password.get())
        messagebox.showinfo("Success", "Credentials saved securely!")
        logging.info("Credentials saved successfully.")
    except Exception as e:
        logging.error(f"Failed to save credentials: {e}")
        messagebox.showerror("Error", f"Failed to save credentials: {e}")

def load_credentials():
    """
    Load sender email and password securely from keyring.
    """
    try:
        saved_password = keyring.get_password("DirectX_Emailer", sender_email.get())
        if saved_password:
            password.delete(0, tk.END)
            password.insert(0, saved_password)
            messagebox.showinfo("Success", "Credentials loaded successfully!")
        else:
            messagebox.showwarning("Warning", "No credentials found for the given email.")
    except Exception as e:
        logging.error(f"Failed to load credentials: {e}")
        messagebox.showerror("Error", f"Failed to load credentials: {e}")

def run_script():
    """
    Collects DirectX info, creates the email, and sends it.
    """
    try:
        dxdiag_output = collect_directx_info()
        msg = create_email(
            sender_email=sender_email.get(),
            receiver_email=receiver_email.get(),
            subject=subject.get(),
            body=body.get("1.0", tk.END),
            attachment_path=dxdiag_output
        )
        send_email(msg, sender_email.get(), password.get())
    except Exception as e:
        logging.error(f"Error in run_script: {e}")
        print(f"Error: {e}")

# GUI Setup
root = tk.Tk()
root.title("DirectX Info Emailer")

# GUI Elements
tk.Label(root, text="Sender Email:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
sender_email = tk.Entry(root, width=40)
sender_email.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Receiver Email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
receiver_email = tk.Entry(root, width=40)
receiver_email.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
password = tk.Entry(root, width=40, show="*")
password.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Subject:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
subject = tk.Entry(root, width=40)
subject.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Body:").grid(row=4, column=0, padx=10, pady=5, sticky="ne")
body = tk.Text(root, width=40, height=10)
body.grid(row=4, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Save Credentials", command=save_credentials).grid(row=5, column=0, pady=10)
tk.Button(root, text="Load Credentials", command=load_credentials).grid(row=5, column=1, pady=10, sticky="w")
tk.Button(root, text="Send Email", command=run_script).grid(row=6, column=0, columnspan=2, pady=20)

# Start the GUI
root.mainloop()