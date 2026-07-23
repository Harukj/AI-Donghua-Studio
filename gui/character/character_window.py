def save_character_profile(self, form_data):
    if not self.selected_character:
        return
    character = self.char_service.get_character_by_name(self.selected_character)
    if character:
        character.name = form_data.get("Tên")
        character.alias = form_data.get("Biệt danh")
        character.gender = form_data.get("Giới tính")
        character.age = form_data.get("Tuổi")
        character.height = form_data.get("Chiều cao")
        character.weight = form_data.get("Cân nặng")
        character.hair = form_data.get("Tóc")
        character.eyes = form_data.get("Mắt")
        character.face = form_data.get("Khuôn mặt")
        character.skin = form_data.get("Màu da")
        character.costume = form_data.get("Trang phục")
        character.weapon = form_data.get("Vũ khí")
        character.personality = form_data.get("Tính cách")
        character.voice = form_data.get("Giọng nói")
        character.style = form_data.get("Style")
        character.positive_prompt = form_data.get("Positive Prompt")
        character.negative_prompt = form_data.get("Negative Prompt")
        character.seed = form_data.get("Mã Seed")
        character.image = form_data.get("Ảnh đại diện")
        character.notes = form_data.get("Ghi chú")
        
        self.db.commit()
        messagebox.showinfo("Studio Commercial", f"Đã lưu đồng bộ 100% hồ sơ thương mại cho '{character.name}'!")
        self.refresh_character_list()
