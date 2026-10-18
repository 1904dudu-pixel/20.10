# OPPO Bắc Ninh — 19 chân dung lấp lánh

Bản nhóm 19 người theo đúng phong cách đã duyệt của nhóm 32: nền `public/photos/ẢNH NỀN.png`, khung bo mềm, tiêu đề Great Vibes “OPPO Bắc Ninh chúc mừng 20/10”, không có nhãn tên riêng. Ảnh Nguyễn Thị Thoa dùng đúng `09_NGUYỄN THỊ THOA.png` theo lựa chọn của người dùng, dù ảnh này đã xuất hiện trong nhóm 32.

Chỉ cắt và thu phóng chân dung từ ảnh gốc. Không tạo ảnh, làm đẹp, chỉnh màu hay dùng AI cho gương mặt. 19 nguồn ảnh, vị trí cắt và hash nằm trong `portraits.json` và `poster-manifest.json`. Bản nhóm 32 và phim chính không thay đổi.

## Video

- 30 giây, lặp mượt, không nhạc; 1.800 khung hình, tốc độ 1×.
- 2560×1440, 60 FPS, MP4 H.264 / libx264, preset `veryfast`, CRF 17, YUV420p, BT.709.
- B-frames 0, GOP 120, video time base 15360, faststart.
- Giữ cấu hình renderer gốc: CRF với bitrate biến thiên, không thay bằng bitrate cố định hoặc cấu hình chất lượng thấp.
- 38 ngôi sao và 58 hạt sáng chuyển động trên nền. Toàn bộ 19 khung chân dung và tiêu đề được bảo vệ khỏi lớp hiệu ứng.

## Xem trước bằng Remotion

Tại thư mục gốc repository, sau `npm ci`:

```bash
npx remotion studio exports/collage-19-animation/index.tsx --public-dir=exports --no-open
```

Chọn composition `OppoGiftCollage19Sparkles`. `spec.json` chứa vị trí, chu kỳ chuyển động và các vùng bảo vệ.

## Xuất lại bằng pipeline FFmpeg gốc

Cài FFmpeg và Python với `numpy`, `Pillow`, rồi chạy từ thư mục gốc repository:

```bash
python3 exports/collage-19-animation/render.py --out exports/OPPO-Bac-Ninh-19-Chan-Dung-Sparkles-1440p60.mp4
```

Renderer kiểm tra hash ảnh nền tổng hợp, pixel được bảo vệ và cấu hình MP4 sau xuất. Remotion và renderer dùng chung `spec.json`.

Có thể dựng lại ảnh tổng hợp 4K từ đúng các ảnh nguồn bằng:

```bash
python3 exports/collage-19-animation/build_poster.py
```

Font Great Vibes kèm giấy phép SIL Open Font License trong `fonts/OFL.txt`.

## Kiểm tra bản xuất

`qa-report.json` ghi kết quả kiểm tra video thực tế: giải mã toàn bộ 1.800 khung hình, không có đoạn hình đen, thời gian khung hình liên tục, kiểm tra đường nối vòng lặp và vùng chân dung được bảo vệ. `release-manifest.json` ghi kích thước và SHA-256 của các file tải.

Để chiếu liên tục, bật Repeat/Loop trong VLC hoặc phần mềm trình chiếu. MP4 không tự bật chế độ lặp của trình phát.
