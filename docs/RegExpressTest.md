# 正規表示式測試用資料

## 鼻音韻母

```sh
keⁿ1
kuaiⁿ5
ia2
uaⁿ2
iau1
liu5
```

## 處理鼻音韻母

1. 將 xnn 轉成 xⁿ

```sh
kenn1
kuainn5
ia2
uann2
iau1
liu5
```

```sh
    - xform/((a|e|i|o|u|ai)nn)/$1ⁿ/
```

2.

```sh
keⁿ1《
kuaiⁿ5《
ia2《
uaⁿ2《
iau1《
liu5《
```

(¹|²|³|⁴|⁵|⁶|⁷|⁸|⁰)
¹²³⁴⁵⁶⁷⁸⁰
[¹²³⁴⁵⁶⁷⁸⁰]
