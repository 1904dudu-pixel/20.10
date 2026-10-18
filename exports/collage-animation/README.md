# OPPO Bắc Ninh — 32 chân dung lấp lánh

Clip 30 giây, lặp liền mạch, không nhạc. 38 ngôi sao và 58 hạt sáng chuyển động trên nền; 32 khung chân dung và tiêu đề được bảo vệ khỏi lớp hiệu ứng.

Nguồn ảnh là bản tiêu đề viết tay đã duyệt: `exports/OPPO-Bac-Ninh-32-Chan-Dung-Tieu-De-Mem-Mai-4K.png`. Không tạo lại, chỉnh màu, làm đẹp hoặc dùng AI với gương mặt.

## Cấu hình xuất đã giữ từ renderer được duyệt

- 2560×1440, 60 FPS, 1.800 khung hình, tốc độ 1×.
- MP4 / libx264, preset `veryfast`, CRF 17, YUV420p, BT.709.
- B-frames 0, GOP 120, video time base 15360, faststart.
- Bản gốc dùng CRF với bitrate biến thiên; không đặt mức bitrate thấp hơn hay đổi sang chế độ nén thấp chất lượng.
- Không thêm âm thanh, theo lựa chọn của người dùng.

## Xem và chỉnh trong Remotion

Tại thư mục gốc repository, sau `npm ci`:

```bash
npx remotion studio exports/collage-animation/index.tsx --public-dir=exports --no-open
```

Chọn composition `OppoGiftCollageSparkles`. Vị trí, chu kỳ sáng, chuyển động và các vùng bảo vệ nằm trong `spec.json`.

## Xuất lại theo đúng pipeline FFmpeg gốc

Cài FFmpeg và Python với `numpy`, `Pillow`, rồi chạy tại thư mục gốc repository:

```bash
python3 exports/collage-animation/render.py --out exports/OPPO-Bac-Ninh-32-Chan-Dung-Sparkles-1440p60.mp4
```

Script kiểm tra hash ảnh gốc trước khi dựng, kiểm tra các pixel được bảo vệ và kiểm tra thông số MP4 sau khi xuất. Composition Remotion dùng cùng `spec.json` để xem trước; bản MP4 được xuất bằng pipeline FFmpeg giữ nguyên thông số chất lượng gốc.

Để chiếu liên tục, bật Repeat/Loop trong VLC hoặc phần mềm trình chiếu. MP4 không tự bật chế độ lặp của trình phát.
