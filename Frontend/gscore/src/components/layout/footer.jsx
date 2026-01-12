const Footer = () => {
    return (
        <footer style={footerStyle}>
            <p>Email: example@gmail.com</p>
            <p>Phone: +84 123 456 789</p>
            <p>Address: 123 Nguyễn Văn A, Hà Nội, Việt Nam</p>
            <p>&copy; 2026 G-Score. All rights reserved.</p>
        </footer>
    )
}

// CSS inline
const footerStyle = {
    position: 'fixed', 
    bottom: 0,
    left: 0,
    width: '100%',
    backgroundColor: '#222',
    color: '#fff',
    textAlign: 'center',
    padding: '10px 0',
};

export default Footer;
