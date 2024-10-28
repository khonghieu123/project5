import streamlit as st
from main import FamilyExpenseTracker, authenticate_user
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_option_menu import option_menu
from pathlib import Path

st.set_page_config(page_title="Quản Lý Chi Tiêu Gia Đình", page_icon="💰")

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

with open(css_file, encoding='utf-8') as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="login-container"><h1>Đăng nhập</h1></div>', unsafe_allow_html=True)
    with st.form(key="login_form"):
        st.markdown('<label>Tên đăng nhập</label>', unsafe_allow_html=True)
        username = st.text_input("", placeholder="Nhập tên đăng nhập của bạn")
        st.markdown('<label>Mật khẩu</label>', unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Nhập mật khẩu của bạn")
        login_button = st.form_submit_button("Đăng nhập")
        if login_button:
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.success("Đăng nhập thành công!")
                st.experimental_rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu.")

if st.session_state.authenticated:
    session_state = st.session_state
    if "expense_tracker" not in session_state:
        session_state.expense_tracker = FamilyExpenseTracker()

    st.markdown('<h1 style="text-align: center;">Quản Lý Chi Tiêu Gia Đình</h1>', unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Nhập Dữ Liệu", "Tổng Quan Dữ Liệu", "Trực Quan Dữ Liệu", "Xuất Dữ Liệu"],
        icons=["pencil-fill", "clipboard2-data", "bar-chart-fill", "file-earmark-spreadsheet"],
        orientation="horizontal",
    )

    expense_tracker = session_state.expense_tracker

    if selected == "Nhập Dữ Liệu":
        st.markdown('<h4 style="text-align: center; color: black;">Thêm Thành Viên Gia Đình</h4>',
                    unsafe_allow_html=True)

        with st.expander("Thêm Thành Viên Gia Đình"):
            st.markdown('<label style="color: black; display: block; margin-bottom: 2px;">Tên</label>',
                        unsafe_allow_html=True)
            member_name = st.text_input("", placeholder="Nhập tên đăng nhập của bạn").title()

            st.markdown('<label style="color: black; display: block; margin-bottom: 2px;">Trạng thái thu nhập</label>',
                        unsafe_allow_html=True)
            earning_status = st.checkbox("")

            st.markdown('<label style="color: black; display: block; margin-bottom: 2px;">Thu nhập</label>',
                        unsafe_allow_html=True)
            earnings = st.number_input("", value=0, min_value=0)

            if st.button("Thêm Thành Viên"):
                try:
                    expense_tracker.add_family_member(member_name, earning_status, earnings)
                    st.success("Thành viên đã được thêm thành công!")
                except ValueError as e:
                    st.error(str(e))

        st.markdown('<h4 style="text-align: center; color: black;">Thêm Chi Phí</h4>', unsafe_allow_html=True)

        with st.expander("Thêm Chi Phí"):
            st.markdown('<label style="color: black;">Danh mục</label>', unsafe_allow_html=True)
            expense_category = st.selectbox("", (
                "Nhà ở", "Thực phẩm", "Giao thông", "Giải trí",
                "Chi phí liên quan đến trẻ em", "Y tế", "Đầu tư", "Khác",
            ))
            st.markdown('<label style="color: black;">Mô tả (tùy chọn)</label>', unsafe_allow_html=True)
            expense_description = st.text_input("").title()
            st.markdown('<label style="color: black;">Giá trị</label>', unsafe_allow_html=True)
            expense_value = st.number_input("", min_value=0)
            st.markdown('<label style="color: black;">Ngày</label>', unsafe_allow_html=True)
            expense_date = st.date_input("", value="today")

            if st.button("Thêm Chi Phí"):
                try:
                    expense_tracker.merge_similar_category(expense_value, expense_category, expense_description,
                                                           expense_date)
                    st.success("Chi phí đã được thêm thành công!")
                except ValueError as e:
                    st.error(str(e))

        st.markdown('<h4 style="text-align: center; color: black;">Đặt Ngân Sách</h4>', unsafe_allow_html=True)
        with st.form(key="budget_form"):
            st.markdown('<label style="color: black;">Chọn Danh Mục</label>', unsafe_allow_html=True)
            budget_category = st.selectbox("", (
                "Nhà ở", "Thực phẩm", "Giao thông", "Giải trí",
                "Chi phí liên quan đến trẻ em", "Y tế", "Đầu tư", "Khác",
            ))
            st.markdown('<label style="color: black;">Số Tiền Ngân Sách</label>', unsafe_allow_html=True)
            budget_amount = st.number_input("", min_value=0)
            if st.form_submit_button("Đặt Ngân Sách"):
                expense_tracker.set_budget(budget_category, budget_amount)
                st.success(f"Ngân sách cho {budget_category} đã được đặt thành {budget_amount}!")

    if selected == "Tổng Quan Dữ Liệu":
        st.markdown('<h1 style="text-align: center; color: black;">Tổng Quan Dữ Liệu</h1>', unsafe_allow_html=True)

        st.header("Thành Viên Gia Đình")

        if not expense_tracker.members:
            st.info("Chưa có thành viên nào được thêm. Vui lòng thêm thành viên từ tab Nhập Dữ Liệu.")
        else:
            members_data = []
            for member in expense_tracker.members:
                members_data.append({
                    "Tên": member.name,
                    "Thu nhập": member.earnings,
                })
            st.dataframe(pd.DataFrame(members_data))

            for member in expense_tracker.members:
                if st.button(f"Xóa {member.name}"):
                    expense_tracker.delete_family_member(member)
                    st.success(f"{member.name} đã được xóa.")
                    st.experimental_rerun()

        st.header("Chi Phí")

        if not expense_tracker.expense_list:
            st.info("Chưa có chi phí nào được thêm. Vui lòng thêm chi phí từ tab Nhập Dữ Liệu.")
        else:
            expenses_data = []
            for expense in expense_tracker.expense_list:
                expenses_data.append({
                    "Danh mục": expense.category,
                    "Giá trị": expense.value,
                    "Mô tả": expense.description,
                    "Ngày": expense.date
                })
            st.dataframe(pd.DataFrame(expenses_data))

            for expense in expense_tracker.expense_list:
                if st.button(f"Xóa {expense.category}"):
                    expense_tracker.delete_expense(expense)
                    st.success(f"Chi phí trong danh mục {expense.category} đã được xóa.")
                    st.experimental_rerun()

        st.markdown('<h2 style="color: black;">Tổng Chi Tiêu</h2>', unsafe_allow_html=True)
        total_expenditure = expense_tracker.calculate_total_expenditure()
        st.write(f"Tổng Chi Tiêu: {total_expenditure}")

    elif selected == "Trực Quan Dữ Liệu":
        st.markdown('<h1 style="text-align: center; color: black;">Trực Quan Dữ Liệu</h1>', unsafe_allow_html=True)
        expense_data = [
            (expense.category, expense.value) for expense in expense_tracker.expense_list
        ]
        if expense_data:
            expenses = [data[0] for data in expense_data]
            values = [data[1] for data in expense_data]
            total = sum(values)
            percentages = [(value / total) * 100 for value in values]

            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                percentages,
                labels=expenses,
                autopct="%1.1f%%",
                startangle=90,
                colors=plt.cm.Paired.colors
            )
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.info("Không có chi phí nào để trực quan. Vui lòng thêm chi phí từ tab Nhập Dữ Liệu.")

    elif selected == "Xuất Dữ Liệu":
        st.header("Xuất Chi Phí ra CSV")
        if st.button("Xuất ra CSV"):
            expense_tracker.export_to_csv()
            st.success("Dữ liệu đã được xuất ra file CSV thành công!")
