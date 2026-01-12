import { useState } from "react";
import { api, endpoints } from "../configs/Apis";

export default function StudentExamResult() {
    const [sbd, setSbd] = useState("");
    const [data, setData] = useState(null);
    const [error, setError] = useState("");

    const handleSearch = async () => {
        try {
            setError("");
            const res = await api.get(`${endpoints.result}${sbd}/`);
            console.log("Data from API:", res.data); 
            setData(res.data); 
        } catch (err) {
            setData(null);
            setError("Không tìm thấy thí sinh hoặc có lỗi API");
            console.error(err);
        }
    };

    const display = (value) => (value !== null && value !== undefined ? value : "–");

    return (
        <div style={{ maxWidth: 600, margin: "40px auto" }}>
            <h2>Tra cứu điểm thi</h2>

            <input
                type="text"
                placeholder="Nhập số báo danh"
                value={sbd}
                onChange={(e) => setSbd(e.target.value)}
                style={{ width: "100%", padding: 10 }}
            />

            <button
                onClick={handleSearch}
                style={{ marginTop: 10, padding: 10, width: "100%" }}
            >
                Tra cứu
            </button>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {data && (
                <table border="1" width="100%" style={{ marginTop: 20 }}>
                    <tbody>
                        <tr>
                            <td>SBD</td>
                            <td>{display(data.registration_number)}</td>
                        </tr>
                        <tr>
                            <td>Toán</td>
                            <td>{display(data.math)}</td>
                        </tr>
                        <tr>
                            <td>Vật lý</td>
                            <td>{display(data.physics)}</td>
                        </tr>
                        <tr>
                            <td>Hóa học</td>
                            <td>{display(data.chemistry)}</td>
                        </tr>
                        <tr>
                            <td>Sinh học</td>
                            <td>{display(data.biology)}</td>
                        </tr>
                        <tr>
                            <td>Ngữ văn</td>
                            <td>{display(data.literature)}</td>
                        </tr>
                        <tr>
                            <td>Ngoại ngữ</td>
                            <td>{display(data.foreign_language)}</td>
                        </tr>
                        <tr>
                            <td>Mã ngoại ngữ</td>
                            <td>{display(data.foreign_language_code)}</td>
                        </tr>
                        <tr>
                            <td>Lịch sử</td>
                            <td>{display(data.history)}</td>
                        </tr>
                        <tr>
                            <td>Địa lý</td>
                            <td>{display(data.geography)}</td>
                        </tr>
                        <tr>
                            <td>Giáo dục công dân</td>
                            <td>{display(data.civic_education)}</td>
                        </tr>
                        {/* Hiển thị khối nếu có */}
                        {data.blocks && Object.entries(data.blocks).map(([block, score]) => (
                            <tr key={block}>
                                <td>Khối {block}</td>
                                <td>{display(score)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}
