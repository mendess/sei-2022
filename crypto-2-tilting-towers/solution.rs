use std::io;
use std::fs::read_to_string;

fn main() -> io::Result<()> {
    let input = read_to_string("input.txt")?;

    let mut flag = Vec::new();
    for chunk in input.as_bytes().chunks(4) {
        let mut shift = 6i32;
        let mut byte = 0u8;
        for c in chunk {
            let nibble = match c {
                b'|' => 0b00,
                b'/' => 0b01,
                b'-' => 0b10,
                b'\\' => 0b11,
                _ => panic!("invalid char: {}", c)
            };
            byte |= nibble << shift;
            shift -= 2;
        }
        flag.push(byte);
    }
    println!("{}", String::from_utf8_lossy(&flag));
    Ok(())
}
