# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest (SimpleVault), TLS 1.3 in transit | ✅ Done | Infra Team |
| Audit logging | CloudTrail + API access logs | ✅ Done | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus + Grafana Alerting) | ✅ Done | Security Team |

## F. TODO: Điền vào phần còn thiếu
Với mỗi row còn "⬜ Todo", mô tả technical solution cụ thể bạn sẽ implement.

### 1. Audit logging (Nhật ký kiểm toán)
- **Technical Solution**:
  - Cấu hình hệ thống logging tập trung sử dụng ELK Stack (Elasticsearch, Logstash, Kibana) hoặc AWS CloudTrail.
  - Sử dụng FastAPI Middleware để tự động ghi nhận log cho mọi API request: ghi lại định danh người dùng (username, role), tài nguyên (resource), hành động (action), IP nguồn, thời điểm yêu cầu, và mã trạng thái HTTP phản hồi.
  - Áp dụng cơ chế phân quyền đọc ghi log nghiêm ngặt và lưu trữ logs trên Storage được bật tính năng Write Once Read Many (WORM) như AWS S3 Object Lock để chống sửa đổi, giả mạo dữ liệu nhật ký kiểm toán.

### 2. Breach detection (Phát hiện xâm phạm)
- **Technical Solution**:
  - Triển khai **Prometheus** thu thập metrics từ FastAPI và server log, đặc biệt giám sát tần suất lỗi `403 Forbidden` và `401 Unauthorized`.
  - Cấu hình **Grafana Alerting / Prometheus Alertmanager** để tự động phát cảnh báo (Alert) đến đội SOC qua Slack, Email hoặc Telegram khi:
    - Số lượng request bị lỗi `403` từ một tài khoản hoặc IP vượt quá 10 lần trong vòng 1 phút (dấu hiệu brute-force hoặc dò quét quyền hạn).
    - Có các mẫu truy xuất dữ liệu bất thường ngoài giờ làm việc hoặc khối lượng tải dữ liệu lớn bất thường.
  - Tích hợp hệ thống phát hiện xâm nhập cấp Host (HIDS) như OSSEC/Wazuh để giám sát các tệp dữ liệu bệnh nhân thô chống truy cập trái phép ở tầng hạ tầng.
