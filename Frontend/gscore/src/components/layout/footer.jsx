const Footer = () => {
    return (
        <footer style={footerStyle}>
            <div style={containerStyle}>
                <div style={sectionStyle}>
                    <h3 style={headingStyle}>G-Score</h3>
                    <p style={descStyle}>Hệ thống tra cứu điểm thi trực tuyến</p>
                </div>
                
                <div style={sectionStyle}>
                    <h4 style={subHeadingStyle}>Liên hệ</h4>
                    <p style={textStyle}>example@gmail.com</p>
                    <p style={textStyle}>+84 123 456 789</p>
                    <p style={textStyle}>123 Nguyễn Văn A, Hà Nội, Việt Nam</p>
                </div>
                
                <div style={sectionStyle}>
                    <h4 style={subHeadingStyle}>Liên kết</h4>
                    <a href="#" style={linkStyle}>Hướng dẫn tra cứu</a>
                    <a href="#" style={linkStyle}>Câu hỏi thường gặp</a>
                    <a href="#" style={linkStyle}>Liên hệ hỗ trợ</a>
                </div>
            </div>
            
            <div style={bottomStyle}>
                <p style={copyrightStyle}>© 2026 G-Score. All rights reserved.</p>
            </div>
        </footer>
    )
}

const footerStyle = {
    marginTop: '60px',
    marginBottom: '0',
    width: '100vw',
    marginLeft: 'calc(-50vw + 50%)',
    backgroundColor: '#1a1a2e',
    color: '#eee',
    padding: '40px 20px 20px',
    borderTop: '3px solid #0f3460',
};

const containerStyle = {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '30px',
    marginBottom: '30px',
};

const sectionStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
};

const headingStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#16c8bb',
    marginBottom: '5px',
};

const subHeadingStyle = {
    fontSize: '18px',
    fontWeight: '600',
    color: '#16c8bb',
    marginBottom: '5px',
};

const descStyle = {
    fontSize: '14px',
    color: '#aaa',
    lineHeight: '1.6',
};

const textStyle = {
    fontSize: '14px',
    color: '#ccc',
    margin: '5px 0',
    lineHeight: '1.6',
};

const linkStyle = {
    fontSize: '14px',
    color: '#ccc',
    textDecoration: 'none',
    margin: '5px 0',
    transition: 'color 0.3s',
    cursor: 'pointer',
};

const bottomStyle = {
    borderTop: '1px solid #333',
    paddingTop: '20px',
    textAlign: 'center',
};

const copyrightStyle = {
    fontSize: '14px',
    color: '#888',
    margin: 0,
};

export default Footer;