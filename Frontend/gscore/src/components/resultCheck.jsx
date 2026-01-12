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

    return (
        <div style={containerStyle}>
            <div style={cardStyle}>
                <h2 style={titleStyle}>Tra cứu điểm thi</h2>

                <input
                    type="text"
                    placeholder="Nhập số báo danh"
                    value={sbd}
                    onChange={(e) => setSbd(e.target.value)}
                    style={inputStyle}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />

                <button onClick={handleSearch} style={buttonStyle}>
                    Tra cứu
                </button>

                {error && <p style={errorStyle}>{error}</p>}

                {data && (
                    <div style={resultContainerStyle}>
                        <div style={headerStyle}>
                            <h3 style={sbdStyle}>SBD: {data.registration_number}</h3>
                        </div>
                        
                        <table style={tableStyle}>
                            <tbody>
                                {data.math != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Toán</td>
                                        <td style={scoreStyle}>{data.math}</td>
                                    </tr>
                                )}

                                {data.physics != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Vật lý</td>
                                        <td style={scoreStyle}>{data.physics}</td>
                                    </tr>
                                )}

                                {data.chemistry != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Hóa học</td>
                                        <td style={scoreStyle}>{data.chemistry}</td>
                                    </tr>
                                )}

                                {data.biology != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Sinh học</td>
                                        <td style={scoreStyle}>{data.biology}</td>
                                    </tr>
                                )}

                                {data.literature != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Ngữ văn</td>
                                        <td style={scoreStyle}>{data.literature}</td>
                                    </tr>
                                )}

                                {data.foreign_language != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Ngoại ngữ</td>
                                        <td style={scoreStyle}>{data.foreign_language}</td>
                                    </tr>
                                )}

                                {data.foreign_language_code != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Mã ngoại ngữ</td>
                                        <td style={scoreStyle}>{data.foreign_language_code}</td>
                                    </tr>
                                )}

                                {data.history != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Lịch sử</td>
                                        <td style={scoreStyle}>{data.history}</td>
                                    </tr>
                                )}

                                {data.geography != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Địa lý</td>
                                        <td style={scoreStyle}>{data.geography}</td>
                                    </tr>
                                )}

                                {data.civic_education != null && (
                                    <tr style={rowStyle}>
                                        <td style={labelStyle}>Giáo dục công dân</td>
                                        <td style={scoreStyle}>{data.civic_education}</td>
                                    </tr>
                                )}

                                {data.blocks &&
                                    Object.entries(data.blocks).map(
                                        ([block, score]) =>
                                            score != null && (
                                                <tr key={block} style={blockRowStyle}>
                                                    <td style={blockLabelStyle}>Khối {block}</td>
                                                    <td style={blockScoreStyle}>{score}</td>
                                                </tr>
                                            )
                                    )}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}

const containerStyle = {
    maxWidth: '700px',
    margin: '40px auto',
    padding: '0 20px',
};

const cardStyle = {
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    padding: '30px',
};

const titleStyle = {
    textAlign: 'center',
    color: '#1a1a2e',
    fontSize: '28px',
    marginBottom: '25px',
    fontWeight: '600',
};

const inputStyle = {
    width: '100%',
    padding: '14px',
    fontSize: '16px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    outline: 'none',
    transition: 'border-color 0.3s',
    boxSizing: 'border-box',
};

const buttonStyle = {
    width: '100%',
    marginTop: '15px',
    padding: '14px',
    fontSize: '16px',
    fontWeight: '600',
    color: '#fff',
    backgroundColor: '#16c8bb',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
};

const errorStyle = {
    color: '#e74c3c',
    textAlign: 'center',
    marginTop: '15px',
    fontSize: '14px',
};

const resultContainerStyle = {
    marginTop: '30px',
    borderTop: '2px solid #f0f0f0',
    paddingTop: '20px',
};

const headerStyle = {
    backgroundColor: '#f8f9fa',
    padding: '15px',
    borderRadius: '8px',
    marginBottom: '20px',
};

const sbdStyle = {
    margin: 0,
    color: '#1a1a2e',
    fontSize: '20px',
    fontWeight: '600',
};

const tableStyle = {
    width: '100%',
    borderCollapse: 'separate',
    borderSpacing: '0 8px',
};

const rowStyle = {
    backgroundColor: '#f8f9fa',
    transition: 'background-color 0.2s',
};

const labelStyle = {
    padding: '12px 16px',
    color: '#555',
    fontSize: '15px',
    fontWeight: '500',
    borderTopLeftRadius: '6px',
    borderBottomLeftRadius: '6px',
};

const scoreStyle = {
    padding: '12px 16px',
    color: '#1a1a2e',
    fontSize: '16px',
    fontWeight: '600',
    textAlign: 'right',
    borderTopRightRadius: '6px',
    borderBottomRightRadius: '6px',
};

const blockRowStyle = {
    backgroundColor: '#e8f5f4',
    transition: 'background-color 0.2s',
};

const blockLabelStyle = {
    padding: '12px 16px',
    color: '#16c8bb',
    fontSize: '15px',
    fontWeight: '600',
    borderTopLeftRadius: '6px',
    borderBottomLeftRadius: '6px',
};

const blockScoreStyle = {
    padding: '12px 16px',
    color: '#16c8bb',
    fontSize: '17px',
    fontWeight: '700',
    textAlign: 'right',
    borderTopRightRadius: '6px',
    borderBottomRightRadius: '6px',
};