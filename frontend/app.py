

x = requests.get(f"{URL_API}/users")
st.write(x.json())

current_user = x.json()[0]["id"]
y = requests.get(f"{URL_API}/users/{current_user}")
st.write("You are logged as " + y.json()["username"])

patient_id = x.json()[1]["id"]
patient_info = requests.get(f"{URL_API}/users/{patient_id}")
st.write("You are logged as " + patient_info.json()["username"])

note = "this is a note from bob"
create_note(3, note)
# st.write(get_notes(patient_id))

user_id = 3
id = 38
st.write("test note by id")
st.write(get_note(user_id, id))

st.write("test modify note from above")
new_note="I've been modified again !"
modify_note(user_id, id, new_note)
st.write("display modified note")
st.write(get_note(user_id, id))

# delete_note(3,38)

if __name__ == '__main__':
    main()