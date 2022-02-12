use itertools::Itertools;
use rand::{distributions::Alphanumeric, Rng};
use std::{
    fs::File,
    io::{self, Write},
};

const FLAG_LEN: usize = 10;
const NOISE_LEN: usize = 500_000 - FLAG_LEN;

fn rand_chars<W: Write>(take: usize, mut into: W) -> io::Result<()> {
    let chunks = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(take)
        .map(char::from)
        .chunks(FLAG_LEN);
    let chars = chunks
        .into_iter()
        .flat_map(|chunks| "SEI{".chars().chain(chunks).chain("}".chars()));

    let mut buf = String::with_capacity(take.min(4096));
    for chunk in &chars.chunks(4096) {
        buf.clear();
        buf.extend(chunk);
        into.write_all(buf.as_bytes())?;
    }
    Ok(())
}

fn main() -> io::Result<()> {
    let mut file = File::create("input")?;
    let cloak = std::str::from_utf8(&[0xe2, 0x81, 0xa3]).unwrap();
    assert_eq!(1, cloak.chars().count());

    let slot = rand::thread_rng().gen_range(100..(NOISE_LEN - 100));

    rand_chars(slot, &mut file)?;

    let mut text = Vec::with_capacity(cloak.len() * 2 + FLAG_LEN + 5);
    text.extend(cloak.bytes());
    rand_chars(FLAG_LEN, &mut text)?;
    std::fs::write("flag", &text[cloak.len()..])?;
    text.extend(cloak.bytes());

    file.write_all(&text)?;

    rand_chars(NOISE_LEN - slot, &mut file)?;

    let mut f = File::create("challenge.md")?;
    f.write_all(
        "# Invisibility Unicloack\n\nEsta é fácil de encontrar, a flag está entre 2 ".as_bytes(),
    )?;
    f.write_all(cloak.as_bytes())?;
    f.write_all(b".\n")?;

    Ok(())
}
