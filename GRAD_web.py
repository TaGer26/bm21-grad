import streamlit as st
from math import sqrt, atan2, degrees

grad_none = [
    (4600, 144, 11.7), (4800, 150, 12.2), (5000, 156, 12.7), (5200, 162, 13.2), (5400, 168, 13.7), (5600, 173, 14.2),
    (5800, 179, 14.7), (6000, 185, 15.2),
    (6200, 191, 15.8), (6400, 197, 16.3), (6600, 203, 16.8), (6800, 209, 17.3), (7000, 215, 17.8), (7200, 221, 18.4),
    (7400, 227, 18.9), (7600, 234, 19.4), (7800, 240, 19.9),
    (8000, 246, 20.5), (8200, 252, 21.0), (8400, 259, 21.6), (8600, 265, 22.1), (8800, 272, 22.7), (9000, 278, 23.2),
    (9200, 285, 23.8), (9400, 291, 24.4), (9600, 298, 24.9),
    (9800, 305, 25.5), (10000, 312, 26.1), (10200, 319, 26.7), (10400, 326, 27.2), (10600, 333, 27.8),
    (10800, 340, 28.5), (11000, 348, 29.0), (11200, 355, 29.7), (11400, 363, 30.3),
    (11600, 370, 30.9), (11800, 378, 31.6), (12000, 386, 32.2), (12200, 394, 32.9), (12400, 402, 33.5),
    (12600, 411, 34.2), (12800, 419, 34.9), (13000, 428, 35.5), (13200, 437, 36.3),
    (13400, 446, 37.0), (13600, 455, 37.7), (13800, 465, 38.5), (14000, 475, 39.3), (14200, 485, 40.1),
    (14400, 496, 40.9), (14600, 507, 41.7), (14800, 519, 42.6), (15000, 531, 43.6),
    (15200, 544, 44.5), (15400, 557, 45.5), (15600, 572, 46.6), (15800, 588, 47.7), (16000, 605, 49.0),
    (16200, 625, 50.4), (16400, 648, 52.0), (16600, 678, 54.0), (16800, 734, 57.7)
]
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

elevation_none = [(4600, 5000, 5), (5000, 10000, 2.3), (10000, 168000, 1)]
elevation_small = [(0, 3000, 4.5), (3000, 4000, 4.25), (4000, 5000, 3), (5000, 8000, 1.5)]
elevation_large = [(0, 3000, 4.4), (3000, 4000, 3.2), (4000, 5500, 1.5)]

rocket_config = {
    "Без тормозного кольца": {
        "id": "1",
        "data": grad_none,
        "elevation": elevation_none,
        "range": "4600м - 16800м"
    },
    "Малое тормозное кольцо": {
        "id": "2",
        "data": grad_small,
        "elevation": elevation_small,
        "range": "2400м - 8000м"
    },
    "Большое тормозное кольцо": {
        "id": "3",
        "data": grad_large,
        "elevation": elevation_large,
        "range": "1600м - 5200м"
    }
}

st.set_page_config(page_title="BM21-GRAD", layout="centered")
rocket_type = st.radio(
    "Тип снаряда:",
    options=list(rocket_config.keys()),
    format_func=lambda x: f"{x} ({rocket_config[x]['range']})"
)
data, elevation_data, rocket_id = rocket_config[rocket_type]["data"], rocket_config[rocket_type]["elevation"], rocket_config[rocket_type]["id"]
col1, col2 = st.columns(2)
with col1:
    grad_x = st.number_input("X РСЗО", value=0)
    grad_y = st.number_input("Y РСЗО", value=0)
    grad_z = st.number_input("Высота РСЗО", value=0)
with col2:
    enemy_x = st.number_input("X Цели", value=0)
    enemy_y = st.number_input("Y Цели", value=0)
    enemy_z = st.number_input("Высота цели", value=0)

if st.button("Рассчитать", type="primary"):
    try:
        elevation_diff = int(enemy_z - grad_z)
        distance = int(sqrt((enemy_x - grad_x) ** 2 + (enemy_y - grad_y) ** 2))
        for elevation_min, elevation_max, value in elevation_data:
            if distance >= elevation_min and distance < elevation_max:
                if rocket_id == "1" and elevation_diff < 100: pass
                else: distance = int(distance + elevation_diff * value)
                break
        else: distance = int(distance + elevation_diff)
        distances = [item[0] for item in data]
        if distance < distances[0] or distance > distances[-1]: st.error("Дистанция вне диапазона!")
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
    except: st.error('Ошибка')