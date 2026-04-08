import customtkinter as ctk
from groq import Groq

# --- Settings ---
# INSERT YOUR API KEY HERE!!!
api_key = "API"
# INSERT YOUR API KEY HERE!!!
client = Groq(api_key=api_key)

def send_message(event=None):
    user_text = entry.get()
    if not user_text.strip():
        return

    # Разблокируем поле, чтобы добавить текст
    chat_box.configure(state="normal")
    chat_box.insert("end", f"Вы: {user_text}\n\n")
    entry.delete(0, "end")

    try:
        # Запрос к нейросети
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "отвечай на русском языке. Отвечай как человек а не википедия, не слишком длинные сообщения, у тебя есть право использовать маты и оскорбления"},
                {"role": "user", "content": user_text}
            ],
        )
        
        
        ai_response = completion.choices[0].message.content
        
        chat_box.insert("end", f"ИИ: {ai_response}\n\n")
    except Exception as e:
        chat_box.insert("end", f"Ошибка: {e}\n\n")

    # Снова блокируем поле и прокручиваем вниз
    chat_box.configure(state="disabled")
    chat_box.see("end")

def clear_chat():
    chat_box.configure(state="normal")
    chat_box.delete("1.0", "end")
    chat_box.configure(state="disabled")

# --- Interface ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Python AI v1.0")
root.geometry("600x600")

# Title
label = ctk.CTkLabel(root, text="🤖 My Personal AI", font=("Arial", 24, "bold"))
label.pack(pady=15)

# Chat window
chat_box = ctk.CTkTextbox(root, width=550, height=400, font=("Arial", 14), wrap="word")
chat_box.pack(padx=20, pady=10)
chat_box.configure(state="disabled")

# Frames
input_frame = ctk.CTkFrame(root, fg_color="transparent")
input_frame.pack(fill="x", padx=25, pady=10)

# Enter
entry = ctk.CTkEntry(input_frame, width=350, placeholder_text="Спроси меня о чем-нибудь...")
entry.pack(side="left", padx=(0, 10))
entry.bind("<Return>", send_message)

# Send button
send_btn = ctk.CTkButton(input_frame, text="Отправить", width=100, command=send_message)
send_btn.pack(side="left", padx=5)

# Clear button
clear_btn = ctk.CTkButton(root, text="Очистить историю", fg_color="transparent", text_color="gray", command=clear_chat)
clear_btn.pack(pady=5)

root.mainloop()
