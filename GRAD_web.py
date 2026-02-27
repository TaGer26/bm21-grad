import streamlit as st
from math import sqrt, atan2, degrees

grad_small = [
    (2400, 151, 8.7), (2600, 163, 9.4), (2800, 175, 10.2), (3000, 187, 10.9), (3200, 200, 11.7),
    (3400, 212, 12.4), (3600, 225, 13.2), (3800, 238, 14.0), (4000, 251, 14.7), (4200, 264, 15.5),
    (4400, 278, 16.3), (4600, 291, 17.1), (4800, 305, 17.9), (5000, 320, 18.7), (5200, 334, 19.6),
    (5400, 349, 20.5), (5600, 365, 21.3), (5800, 381, 22.3), (6000, 398, 23.2), (6200, 415, 24.2),
    (6400, 433, 25.2), (6600, 452, 26.2), (6800, 472, 27.3), (7000, 493, 28.4), (7200, 517, 29.7),
    (7400, 542, 31.0), (7600, 571, 32.5), (7800, 605, 34.2), (8000, 649, 36.3)
]

grad_large = [
    (1600, 150, 7.2), (1800, 169, 8.1), (2000, 188, 9.0), (2200, 208, 9.9),
    (2400, 227, 10.9), (2600, 248, 11.9), (2800, 268, 12.8), (3000, 290, 13.8),
    (3200, 312, 14.9), (3400, 335, 15.9), (3600, 359, 17.0), (3800, 384, 18.1),
    (4000, 410, 19.3), (4200, 439, 20.6), (4400, 470, 22.0), (4600, 504, 23.4),
    (4800, 543, 25.0), (5000, 591, 27.0), (5200, 660, 29.7)
]

elevation_k = [(0, 3000, 4.4, 4.5), (3000, 4000, 3.2, 4.25), (4000, 5000, 1.5, 3), (5000, 8000, 1.5, 1.5)]

st.set_page_config(page_title="BM21-GRAD", layout="centered")

rocket_type = st.radio(
    "Тип снаряда:",
    options=["1", "2"],
    format_func=lambda
        x: "9М22 ОФ Малое тормозное кольцо (2400м - 8000м)" if x == "1" else "9М22 ОФ Большое тормозное кольцо (1600м - 5200м)"
)
data = grad_small if rocket_type == "1" else grad_large
col1, col2 = st.columns(2)
with col1:
    st.subheader("Позиция РСЗО", anchor=False)
    grad_x = st.number_input("X РСЗО", value=0)
    grad_y = st.number_input("Y РСЗО", value=0)
    grad_z = st.number_input("Z РСЗО", value=0)
with col2:
    st.subheader("Позиция противника", anchor=False)
    enemy_x = st.number_input("X ПРОТИВНИКА", value=0)
    enemy_y = st.number_input("Y ПРОТИВНИКА", value=0)
    enemy_z = st.number_input("Z ПРОТИВНИКА", value=0)
if st.button("Рассчитать", type="primary"):
    try:
        elevation = int(enemy_z - grad_z)
        distance = int(sqrt((enemy_x - grad_x) ** 2 + (enemy_y - grad_y) ** 2))
        for elevation_min, elevation_max, value_l, value_s in elevation_k:
            if distance >= elevation_min and distance < elevation_max:
                if rocket_type == "1": distance = int(distance + elevation * value_s)
                else: distance = int(distance + elevation * value_l)
                break
        else:
            distance = int(distance + elevation * 3)
        distances = [item[0] for item in data]
        if distance < distances[0] or distance > distances[-1]:
            st.error("Дистанция вне диапазона!")
        else:
            for i in range(len(distances) - 1):
                if distances[i] < distance < distances[i + 1]:
                    first_data = data[i]
                    last_data = data[i + 1]
                    break

            grad_elevation = int(first_data[1] + ((distance - first_data[0]) * ((last_data[1] - first_data[1]) / 200)))
            azimuth_mils = int(((90 - (degrees(atan2(enemy_y - grad_y, enemy_x - grad_x)))) % 360) * 6000 / 360)

            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1: st.metric("Азимут", f"{azimuth_mils} тыс")
            with col_res2: st.metric("Угол подъема", f"{grad_elevation} тыс")
            with col_res3: st.metric("Дистанция", f"{distance} м")
            st.divider()
            col_info1, col_info2 = st.columns(2)
            with col_info1: st.info(f"Время полета: {last_data[2]} с")
            with col_info2: st.info(f"Корректировка на 100м: {(last_data[1] - first_data[1]) // 2} тыс")
    except: st.error("Ошибка")