def combine(google,csv,naver):
    
    google.update(csv)
    if naver is not None:
        google['types'].append(naver)

    return google

