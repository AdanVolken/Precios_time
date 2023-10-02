from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Configuración de Selenium
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument("--accept-all-cookies")
driver_path = 'C:\\driver_internet\\chromedriver.exe'  # Ruta al controlador de Chrome

# Inicializar el navegador
driver = webdriver.Chrome(options=chrome_options)

# Producto a buscar
producto = input("¿Qué producto desea buscar?: ")

# Navega a la página web de Mercado Libre
driver.get("https://www.mercadolibre.com.ar/")

# Ingresa la búsqueda "pelota de futbol"
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "as_word"))).send_keys(producto)

# Haz clic en el botón de búsqueda
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.nav-search-btn"))).click()

nombres = []
precios = []

numero_pagina = 1

while True:
    # Espera a que se carguen los resultados de búsqueda
    elementos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ui-search-result__content-wrapper")))

    for elemento in elementos:
        nombre_producto = elemento.find_element(By.CLASS_NAME, "ui-search-item__title.shops__item-title").text
        precio_producto = elemento.find_element(By.CLASS_NAME, "andes-money-amount__fraction").text
        nombres.append(nombre_producto)
        precios.append(precio_producto)

    try:
            # Intenta encontrar el botón de siguiente página y hacer click en él
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Siguiente']"))).click()
            # next_button = driver.find_element(By.XPATH, "//a[@title='Siguiente']")
            # next_button.click()

            numero_pagina += 1
    except:
        # Si no se encuentra el botón de siguiente página, termina el bucle
        print("NOESTAS ENTRANDO BIEN FLACO ")
        break

# Cierra el navegador cuando hayas terminado
driver.quit()

#Creamos el archivo excel para ver los productos
df_mercado = pd.DataFrame({"Productos": nombres , "Precio":precios})

# df_mercado.to_excel("Lista_Mercado_Libre.xlsx", index=False)

# Reemplaza cualquier carácter no numérico (como punto y coma) por una cadena vacía
df_mercado['Precio'] = df_mercado['Precio'].str.replace('[^\d]', '', regex=True)

# Convierte la columna 'Precio' a tipo entero (int)
df_mercado['Precio'] = df_mercado['Precio'].astype(int)

media = df_mercado["Precio"].mean()

print(media)

maximo = media * 2

minimo = media / 2

resultado = df_mercado[(df_mercado['Precio'] > minimo) & (df_mercado['Precio'] < maximo)]


# Cree un archivo Excel con los resultados filtrados
resultado.to_excel("Mercado_Libre.xlsx", index=False)