### Утилита для реконструкции ЦМР в зонах обрушения береговой линии  

аргументы:
    
    iname= - имя файла ЦМР  
    vname= - имя векторного слоя с линией, от которой проводится восстановление  
    mname= - имя векторого слоя с полигоном для маскировки не изменяемых участков  
    oname= - имя файлв для сохрвнения результата   
    kernel= - размер фильтра для восстановления (3 или 5), по умолчанию 3  
    niter= - количество итерации реконструкции, по умолчанию 1  
    --clip_negative - флаг, првести отрицательные значения высот к 0  

---
### пример:  
<code>$ python reconstruct_dem.py iname=./data/dem_clip.tif vname=./data/rec_line.shp mname=./data/inside.shp oname=./data/reconstructed.tif kernel=3 niter=5 --clip_negative</code>

#### исходный ЦМР и линия границы для восстановления
![Source](doc/pics/source.png?raw=true)
#### результат реконструкции
![Reconstructed](doc/pics/rec.png?raw=true)

---

### Dependencies

* GDAL
* numpy
* scipy

