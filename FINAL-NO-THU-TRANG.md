# OPPO Bắc Ninh – Final No Thu Trang

Bản gốc: Final Polished, commit `5bb41c1dd9c66fffbc16b197a12d7e0d16c1765b`, workflow thành công `38909593711`. Video gốc dài 549,333333 giây (09:09.333), 32960 frame.

Chỉ loại cảnh `photo-49`, nguồn `public/photos/10_ĐINH THỊ THU TRANG.png`. File ảnh gốc vẫn được giữ. Còn **51 ảnh, 16 lời chúc nam, 74 cảnh**, **32627 frame / 543,783333 giây (09:03.783)**. Mỗi ảnh vẫn 360 frame / 6 giây; crossfade vẫn 27 frame / 0,45 giây. Vì hai cảnh chồng 0,45 giây, bỏ một ảnh làm ngắn **333 frame / 5,55 giây**.

Giữ số hiệu ảnh gốc 1–48, 50–52 để giữ nguyên nhóm, thứ tự, hướng zoom và cache hiệu ứng. `photo-48` nối trực tiếp `photo-50` tại **07:31.583–07:32.033** theo cùng smoothstep crossfade. Các cảnh phía sau dịch sớm 333 frame, không thay đổi thời lượng riêng. Nhóm cuối còn 12 ảnh. Lời nói của nhóm nam 04 bắt đầu **07:50.733**; Outro bắt đầu **08:43.783**.

## Đồng bộ âm thanh

Dùng lại soundtrack thực tế từ MP4 Final Polished đã render thành công. Workflow tải đúng artifact cũ và xác minh SHA-256 `259c35c457bc5b5ac2adf159bde1047cb0a11c88f4b4e14ff48dca025084b2c8` trước khi biên tập. Không chạy trình tạo instrumental, không xử lý lại giọng, không normalize, không đổi gain hoặc tốc độ.

Rút 5,55 giây ở đuôi không lời trước điệp khúc, tương ứng 07:25.000–07:30.550 của bản gốc. Crossfade smoothstep 0,65 giây, cửa sổ ở timeline mới **07:24.675–07:25.325**. Đây là coda đã kết thúc câu hát, không có phát biểu của nhân sự. Mọi mẫu PCM trước 07:24.675 và từ 07:25.325 trở đi khớp chính xác soundtrack gốc sau khi bù độ lệch 5,55 giây; chỉ cửa sổ nối được blend.

Toàn bộ điệp khúc đã duyệt **199,68–223,26 giây của NHẠC 20.10.mp3**, dài **23,58 giây**, được giữ đầy đủ. Vị trí phát mới **07:25.450–07:49.030** (cũ 07:31.000–07:54.580). Fade, mức nhạc, ducking, phần cao trào và lời hát đều lấy nguyên từ bản mix được duyệt. Nhạc lời chúc và nhạc Outro cũng được dịch nguyên khối; điểm đồng bộ logo/nhạc trong Outro giữ nguyên.

## Kiểm tra và xuất

`preflight.py` đối chiếu toàn bộ dữ liệu từng cảnh với snapshot Final Polished: chỉ thiếu `photo-49`, chỉ thay mốc tuyệt đối của cảnh phía sau; giữ nguyên toàn bộ nguồn, tên/chức vụ, điểm cắt, tốc độ, hướng hình, layout và hiệu ứng. Giữ nguyên `render.py`, `motion.json`, mã React và các file ảnh/video/nhạc nguồn.

Preview `01-photo-removal-and-chorus.mp4` phủ **07:20.000–07:53.733** của timeline mới. Render toàn bộ chỉ chạy sau khi preview giải mã được và khớp âm thanh. QA kiểm tra 51 ảnh, 16 video, frame thực tế của đủ 74 cảnh so với scene và MP4 Final Polished, âm thanh từng người, true peak, khoảng lặng, blackdetect và giải mã toàn bộ MP4. Đồng thời so sánh payload SHA-256 của toàn bộ 32600 frame H.264 ngoài chuyển cảnh mới (27 frame), yêu cầu khớp bản gốc sau khi bù 333 frame đã bỏ. Kết quả thực tế nằm trong `qa-report.json` của artifact, không coi việc tạo manifest là render thành công.

Xuất đúng pipeline hiện có: **H.264, 2560×1440, 60 FPS, CRF 17, preset veryfast; AAC stereo 48 kHz, 320 kb/s**. Không thay thiết lập nén video. File `out/oppo-bac-ninh-20-10-final-no-thu-trang-1440p60.mp4`.

Artifact: **OPPO-Bac-Ninh-20-10-Final-No-Thu-Trang-1440p60**, lưu 14 ngày, chỉ upload sau khi QA thành công. Có thêm bundle `…-QA` nhỏ để tải preview và báo cáo riêng.

## Chạy lại trên máy tính

Cài Node.js 22+, Python 3.12+, FFmpeg và font DejaVu. Tải/lưu MP4 Final Polished đã duyệt trước khi artifact cũ hết hạn, rồi đặt biến `APPROVED_POLISHED_MP4` tới file đó. Script yêu cầu đúng SHA đã ghi nhận; không tự tạo lại nhạc khi thiếu bản gốc.

```bash
npm ci
python3 -m pip install -r scripts/final/requirements.txt
export APPROVED_POLISHED_MP4=/duong/dan/oppo-bac-ninh-20-10-final-polished-1440p60.mp4
npm run render:fast
npm run verify:render
```

Bản `FINAL-POLISHED.md` và snapshot các giai đoạn trước giữ làm hồ sơ lịch sử; lệnh render hiện tại dùng `src/data/final-manifest.json` có 51 ảnh.
