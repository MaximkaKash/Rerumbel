import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECRET_KEY = 'django-insecure-&s!@i3ivvjj-)___&w_(k%)hfjn58jdc2ma(8nzm+&9l_f#ftr'
with open('/../../venv/SECRET_KEY.txt') as f:
    SECRET_KEY = f.read().strip()

# SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

STATICFILES_DIRS = [os.path.join(BASE_DIR, "Front/Main"),
                    os.path.join(BASE_DIR, "Front/Personal")]
STATIC_DIR = os.path.join(BASE_DIR, "static")
