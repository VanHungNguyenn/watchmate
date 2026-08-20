# Docker — Ghi chú sử dụng

Môi trường **phát triển** cho dự án watchmate (Django 6.1 + DRF + SQLite).

> Đây là setup dev, không dùng cho production. Xem phần [Lưu ý](#lưu-ý) ở cuối.

---

## Bắt đầu nhanh

```bash
docker compose up -d          # khởi động (chạy nền)
```

Mở http://localhost:8000/movie/list/

```bash
docker compose down           # dừng lại
```

Lần đầu chạy sẽ mất vài phút để tải Python và cài thư viện. Các lần sau chỉ vài giây.

---

## Chạy / dừng

| Lệnh | Việc gì |
|---|---|
| `docker compose up` | Chạy, hiện log trực tiếp trên terminal (Ctrl+C để dừng) |
| `docker compose up -d` | Chạy nền, trả lại terminal ngay |
| `docker compose up -d --build` | Build lại image rồi chạy |
| `docker compose down` | Dừng và xoá container |
| `docker compose restart web` | Khởi động lại (tự chạy `migrate` lại) |
| `docker compose ps` | Container có đang chạy không? |

**Khi nào cần `--build`:**
- Sửa `requirements.txt` (thêm/bớt thư viện) → **cần**
- Sửa `Dockerfile` → **cần**
- Sửa file `.py` → **không cần**, Django tự reload

---

## Xem log

```bash
docker compose logs -f web    # theo dõi liên tục
docker compose logs --tail 50 web
```

`Ctrl+C` khi đang xem `logs -f` chỉ thoát khỏi việc xem — **server vẫn chạy**.
Muốn dừng server thật thì `docker compose down`.

Log này hiện cả request đến và traceback lỗi — chỗ đầu tiên cần soi khi có bug.

---

## Lệnh Django (manage.py)

Cú pháp chung: `docker compose exec web python manage.py <lệnh>`

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell
docker compose exec web python manage.py showmigrations
docker compose exec web python manage.py test
```

File migration sinh ra sẽ **tự xuất hiện trong thư mục dự án** trên máy bạn
(nhờ volume mount), commit git được luôn.

### Gõ tắt

Thêm vào `~/.zshrc`:

```bash
alias dm="docker compose exec web python manage.py"
```

Chạy `source ~/.zshrc`, sau đó:

```bash
dm makemigrations
dm migrate
dm createsuperuser
```

### Vào shell trong container

```bash
docker compose exec web sh
# đang ở /app, gõ lệnh tự nhiên:
python manage.py makemigrations
exit
```

---

## `exec` và `run` khác gì nhau

`exec` cần container **đang chạy**. Nếu chưa `up` sẽ báo lỗi "service not running".

Khi container chưa chạy, dùng `run` để tạo container tạm:

```bash
docker compose run --rm web python manage.py makemigrations
```

`--rm` dọn container tạm sau khi xong (không có thì container rác tích dần).

Thực tế: `up -d` một lần đầu ngày, rồi dùng `exec` cả ngày.

---

## Luồng làm việc thường ngày

```bash
# đầu ngày
docker compose up -d

# sửa code .py → không cần làm gì, tự reload

# sau khi sửa models.py
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# sau khi thêm thư viện vào requirements.txt
docker compose up -d --build

# cuối ngày
docker compose down
```

---

## Xử lý sự cố

**Cổng 8000 bị chiếm** — đổi số bên trái trong `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"      # truy cập localhost:8001
```

Số bên phải phải giữ `8000` (cổng Django đang nghe bên trong container).

**Thư viện mới cài mà báo `ModuleNotFoundError`** — chưa build lại:

```bash
docker compose up -d --build
```

**Muốn xoá database làm lại từ đầu:**

```bash
docker compose down
rm db.sqlite3
docker compose up -d          # migrate tự chạy, tạo DB mới
```

**Build lại sạch hoàn toàn (bỏ hết cache):**

```bash
docker compose build --no-cache
```

**Container khởi động rồi tắt ngay** — xem lỗi ở đâu:

```bash
docker compose logs web
```

---

## Các file liên quan

| File | Vai trò |
|---|---|
| `Dockerfile` | Công thức tạo image: Python 3.13 + thư viện + code |
| `docker-compose.yml` | Cách chạy: cổng, volume, lệnh khởi động |
| `requirements.txt` | Thư viện Python (ghim cứng version) |
| `.dockerignore` | Loại file không cần copy vào image |

Vài điểm đáng biết:

- **Volume `.:/app`** — thư mục dự án được dùng chung giữa máy bạn và container.
  Nên sửa code là container thấy ngay, và `db.sqlite3` do container tạo nằm
  trên máy bạn (xoá container không mất dữ liệu).
- **`0.0.0.0:8000`** trong lệnh runserver là bắt buộc. Mặc định Django bind
  `127.0.0.1`, chỉ nghe từ bên trong container → trình duyệt trên máy bạn
  không vào được.
- **DRF phải từ 3.18.0 trở lên** để tương thích Django 6.1. Bản 3.16.x crash
  với lỗi `cannot import name 'cc_delim_re'`.

---

## Lưu ý

Setup này dành cho phát triển:

- `runserver` là server dev của Django — chậm, không chịu được traffic thật
- `DEBUG = True` sẽ phơi mã nguồn ra trang lỗi
- `SECRET_KEY` đang để cứng trong `watchmate/settings.py`
- SQLite không phù hợp nhiều người dùng đồng thời

Khi cần deploy thật sẽ cần cấu hình khác: gunicorn thay `runserver`,
Postgres thay SQLite, secrets truyền qua biến môi trường, `DEBUG = False`.
