import remote_update

remote_update.listen("password", __file__, True)

demo = input("Who are you?")
print(f"Hello {demo}.\n:-)")