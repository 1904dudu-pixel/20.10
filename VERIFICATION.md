# Kết quả kiểm tra video 20/10

Bản MP4 đã được xuất và kiểm tra trong môi trường làm việc ngày 16/10/2026.
Bản bàn giao dùng đường xuất FFmpeg từ timeline của dự án Remotion.

- H.264 / yuv420p, 2560 × 1440, 60 fps, 15.189 frame.
- Thời lượng 253,15 giây; file kiểm tra 594.639.182 byte.
- AAC stereo 48 kHz, cấu hình 320 kbps, đúng `public/music/NHẠC 20.10.mp3`.
- Giải mã toàn bộ hình và âm thanh: đạt, không gặp lỗi decoder.
- 52/52 khung hình giữa cảnh khớp đúng ảnh gốc; không thiếu/lặp/sai thứ tự.
- Ảnh chứa nguyên thiết kế, tên, chân dung, lời chúc; không có ảnh SVG mẫu trên timeline.
- Tương quan ảnh thấp nhất: 0.97864; ở mỗi cảnh ảnh mong đợi là ảnh khớp tốt nhất trong cả 52 nguồn.
- Intro 8,3 giây và Outro 20 giây: khớp đúng video nguồn, giữ nguyên tốc độ/thời lượng.
- Đối chiếu nhạc tại 49 vị trí: tương quan thấp nhất 0.99988.
- Fade-in 1,5 giây, fade-out 3 giây: đạt kiểm tra biên độ.
- Đỉnh mẫu stereo tại 48 kHz: 0.83567, dưới ngưỡng clipping 1,0.
- TypeScript, ESLint, build bundle Remotion và render khung hình thử: đạt.

Kiểm tra clipping đo riêng hai kênh stereo ở sample rate gốc. Không dùng mức đỉnh
của bản downmix mono, vì phép cộng hai kênh có thể vượt 1,0 dù từng kênh không clipping.

Chạy lại `npm run verify:render` sau khi xuất video để có báo cáo JSON cho chính file đó.
Mỗi lượt GitHub Actions chỉ tải artifact lên khi bước kiểm tra của lượt đó thành công.
Báo cáo chi tiết và danh sách ảnh/timestamp được gói cùng MP4 trong artifact.

## Cách lấy video

Đọc [README](README.md) để tải artifact GitHub hoặc xuất trên máy với Node.js 22 trở lên:

```bash
npm ci
npm run render
```

Kết quả: `out/oppo-bac-ninh-20-10-1440p60.mp4`.
Nếu có FFmpeg bản đầy đủ trong PATH, dùng `npm run render:fast` để xuất nhanh hơn.
