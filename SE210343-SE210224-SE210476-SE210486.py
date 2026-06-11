"""
BÀI TẬP THỰC HÀNH
XỬ LÝ LIST VÀ STRING TRONG PYTHON
Chủ đề: Quản lý danh sách sinh viên cơ bản

Yêu cầu:
- Sinh viên KHÔNG được thay đổi hàm main().
- Sinh viên chỉ bổ sung mã nguồn vào các vị trí TODO.
- Không sử dụng thư viện ngoài.
- Bài tập tập trung vào list, string, vòng lặp, điều kiện và hàm.
"""


# ============================================================
# 1. CHUẨN HÓA HỌ TÊN SINH VIÊN
# ============================================================

def normalize_name(name):
    """
    Chuẩn hóa họ tên sinh viên.

    Yêu cầu:
    - Xóa khoảng trắng thừa ở đầu và cuối chuỗi.
    - Chuẩn hóa nhiều khoảng trắng giữa các từ thành một khoảng trắng.
    - Viết hoa chữ cái đầu của mỗi từ.

    Ví dụ:
    normalize_name("  nguyen   van an  ")
    Kết quả: "Nguyen Van An"
    """

    # TODO: Hoàn thiện hàm normalize_name
    def normalize_name(name):
        tach=name.split()
        noi=" ".join(tach)
        return noi.title()
    a=normalize_name("  nguyen   van an  ")
    print(a)


# ============================================================
# 2. KIỂM TRA ĐIỂM HỢP LỆ
# ============================================================

def is_valid_score(score):
    """
    Kiểm tra điểm có hợp lệ hay không.

    Điểm hợp lệ là điểm nằm trong khoảng từ 0 đến 10.

    Trả về:
    - True nếu điểm hợp lệ.
    - False nếu điểm không hợp lệ.
    """

    # TODO: Hoàn thiện hàm is_valid_score
    def is_valid_score(score):
        return 0 <= score  <= 10


# ============================================================
# 3. THÊM SINH VIÊN VÀO DANH SÁCH
# ============================================================

def add_student(names, scores, name, score):
    """
    Thêm một sinh viên vào hai danh sách names và scores.

    Yêu cầu:
    - Chuẩn hóa họ tên trước khi thêm.
    - Chỉ thêm sinh viên nếu điểm hợp lệ.
    - Nếu thêm thành công, trả về True.
    - Nếu điểm không hợp lệ, không thêm và trả về False.
    """

    # TODO: Hoàn thiện hàm add_student
    result = " ".join(name.strip().split()).lower().title()
    names.append(result)
    
    if 0 <= score <= 10:
        scores.append(round(score, 1))
    else:
        return False
    
    return names, scores


# ============================================================
# 4. HIỂN THỊ DANH SÁCH SINH VIÊN
# ============================================================

def display_students(names, scores):
    """
    Hiển thị danh sách sinh viên.

    Định dạng mỗi dòng:
    1. Nguyen Van An - Diem: 8.5
    """

    # TODO: Hoàn thiện hàm display_students
    for i in range(len(names)):
        print(f"{i + 1}. {names[i].title()} - Diem: {scores[i]}")


# ============================================================
# 5. TÍNH ĐIỂM TRUNG BÌNH
# ============================================================

def calculate_average_score(scores):
    """
    Tính điểm trung bình của danh sách điểm.

    Trả về:
    - Điểm trung bình nếu danh sách không rỗng.
    - 0 nếu danh sách rỗng.
    """

    # TODO: Hoàn thiện hàm calculate_average_score
    if len(scores)==0:
        return 0
    else: 
        return sum(scores) / len(scores)



# ============================================================
# 6. TÌM SINH VIÊN CÓ ĐIỂM CAO NHẤT
# ============================================================

def find_highest_score_student(names, scores):
    """
    Tìm sinh viên có điểm cao nhất.

    Trả về:
    - Tuple dạng (name, score) nếu danh sách không rỗng.
    - None nếu danh sách rỗng.
    """

    # TODO: Hoàn thiện hàm find_highest_score_student
    if not scores:   
        return None
        
    max_score = scores[0]
    max_index = 0
    
    for i in range(1, len(scores)):
        if scores[i] > max_score:
            max_score = scores[i]
            max_index = i
            
    return (names[max_index], scores[max_index])


# ============================================================
# 7. TÌM KIẾM SINH VIÊN THEO TỪ KHÓA
# ============================================================

def find_students_by_keyword(names, scores, keyword):
    """
    Tìm sinh viên có họ tên chứa keyword.

    Yêu cầu:
    - Không phân biệt chữ hoa/chữ thường.
    - Trả về danh sách các tuple dạng (name, score).
    - Nếu không tìm thấy, trả về danh sách rỗng.

    Ví dụ:
    keyword = "thi"
    Có thể tìm thấy "Tran Thi Binh" và "Ho Thi Em".
    """

    # TODO: Hoàn thiện hàm find_students_by_keyword
    result = []
    lower_name = []
    
    for name in names:
        lower_name.append(name.lower())
    
    for name_position in range(len(lower_name)):
        
        if keyword.lower() in lower_name[name_position]:
            score = scores[name_position]
            result.append((names[name_position].title(),score))
    return result

# ============================================================
# 8. LỌC SINH VIÊN ĐẠT ĐIỂM THEO NGƯỠNG
# ============================================================

def get_passed_students(names, scores, threshold):
    """
    Lấy danh sách sinh viên có điểm lớn hơn hoặc bằng threshold.

    Trả về:
    - Danh sách các tuple dạng (name, score).
    """

    # TODO: Hoàn thiện hàm get_passed_students
    results_threshold=[]
    for index  in range (len(names)):
        if scores[index] >= threshold:
            results_threshold.append(
                    (names[index],  scores[index])
                    )
    return results_threshold



# ============================================================
# 9. SẮP XẾP SINH VIÊN THEO HỌ TÊN
# ============================================================

def sort_students_by_name(names, scores):
    """
    Sắp xếp sinh viên theo họ tên tăng dần.

    Yêu cầu:
    - Trả về hai danh sách mới: sorted_names và sorted_scores.
    - Không làm thay đổi trực tiếp danh sách names và scores ban đầu.

    Gợi ý:
    - Có thể dùng thuật toán sắp xếp đơn giản bằng hai vòng lặp.
    - Khi đổi vị trí tên, cần đổi vị trí điểm tương ứng.
    """

    # TODO: Hoàn thiện hàm sort_students_by_name
    ghep_ten_so = list(zip(names, scores))   
    xep = sorted(ghep_ten_so, key=lambda student: student[0].split()[-1])
    sorted_names, sorted_scores = zip(*xep) 
    return list(sorted_names), list(sorted_scores)



# ============================================================
# 10. TẠO EMAIL TỪ HỌ TÊN
# ============================================================

def create_email_from_name(name):
    """
    Tạo email sinh viên từ họ tên.

    Quy tắc:
    - Chuẩn hóa họ tên.
    - Chuyển toàn bộ sang chữ thường.
    - Các từ được nối với nhau bằng dấu chấm.
    - Thêm đuôi @student.edu.vn.

    Ví dụ:
    create_email_from_name("Nguyen Van An")
    Kết quả: "nguyen.van.an@student.edu.vn"
    """

    # TODO: Hoàn thiện hàm create_email_from_name
    words = name.split()     
    lower_words = [word.lower() for word in words]
    email_prefix = ".".join(lower_words)
    return f"{email_prefix}@student.edu.vn"


# ============================================================
# CÂU NÂNG CAO: XÓA SINH VIÊN THEO HỌ TÊN
# ============================================================

def remove_student_by_name(names, scores, name):
    """
    Xóa sinh viên theo họ tên.

    Yêu cầu:
    - So sánh tên không phân biệt chữ hoa/chữ thường.
    - Nên chuẩn hóa tên trước khi so sánh.
    - Nếu tìm thấy, xóa sinh viên khỏi cả names và scores.
    - Nếu xóa thành công, trả về True.
    - Nếu không tìm thấy, trả về False.
    """

    # TODO: Hoàn thiện hàm remove_student_by_name
    result = find_students_by_keyword(names, scores, name)
    
    if result:    
        found_name = result[0][0]

        index = None
        for i in range(len(names)):
            if names[i].lower() == found_name.lower():
                index = i
                break

        if index is not None:
            names.pop(index)
            scores.pop(index)
            return True
        
    return False


# ============================================================
# HÀM HỖ TRỢ IN DANH SÁCH TUPLE
# Sinh viên không cần chỉnh sửa hàm này.
# ============================================================

def print_student_tuples(student_list):
    """
    In danh sách sinh viên dạng tuple (name, score).
    """
    if not student_list:
        print("Khong co sinh vien")
        return

    for name, score in student_list:
        print(f"{name} - Diem: {score}")


# ============================================================
# HÀM MAIN
# Sinh viên KHÔNG được thay đổi hàm main().
# ============================================================

def main():
    names = []
    scores = []

    sample_data = [
        ("  nguyen   van an  ", 8.5),
        ("TRAN thi binh", 9.2),
        ("le MINH chau", 6.8),
        ("pham hoang dung", 4.5),
        ("ho thi em", 7.5),
    ]

    for name, score in sample_data:
        add_student(names, scores, name, score)

    print("=== DANH SACH SINH VIEN ===")
    display_students(names, scores)

    print("\n=== DIEM TRUNG BINH ===")
    average_score = calculate_average_score(scores)
    print(round(average_score, 2) if average_score is not None else None)

    print("\n=== SINH VIEN CO DIEM CAO NHAT ===")
    highest_student = find_highest_score_student(names, scores)
    if highest_student is not None:
        name, score = highest_student
        print(f"{name} - Diem: {score}")
    else:
        print("Danh sach rong")

    print("\n=== TIM KIEM TU KHOA 'thi' ===")
    search_result = find_students_by_keyword(names, scores, "thi")
    print_student_tuples(search_result)

    print("\n=== SINH VIEN DAT DIEM >= 5.0 ===")
    passed_students = get_passed_students(names, scores, 5.0)
    print_student_tuples(passed_students)

    print("\n=== DANH SACH SAP XEP THEO TEN ===")
    sorted_result = sort_students_by_name(names, scores)
    if sorted_result is not None:
        sorted_names, sorted_scores = sorted_result
        display_students(sorted_names, sorted_scores)
    else:
        print("Chua cai dat chuc nang sap xep")

    print("\n=== EMAIL SINH VIEN ===")
    for name in names:
        email = create_email_from_name(name)
        print(f"{name} -> {email}")

    print("\n=== XOA SINH VIEN 'Pham Hoang Dung' ===")
    is_removed = remove_student_by_name(names, scores, "Pham Hoang Dung")
    print("Xoa thanh cong" if is_removed else "Khong tim thay sinh vien")

    print("\n=== DANH SACH SAU KHI XOA ===")
    display_students(names, scores)


if __name__ == "__main__":
    main()
