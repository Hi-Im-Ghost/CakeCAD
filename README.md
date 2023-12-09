# Konfiguracja
Wejdź se do foldera w konsoli anakundy a następnie rób to</br>
```
conda create -n pyoccenv python=3.8</br>
conda activate pyoccenv</br>
conda install -c conda-forge pythonocc-core</br>
pip install tornado</br>
python -c "import OCC; print(OCC.VERSION)"</br>
```
</br>
Jak zadziała i wyświetli się wersja zamiast błędu to odpalaj</br>
```
python main.py
```