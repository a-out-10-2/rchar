// -*- coding: utf-8 -*-
// -----------------------------------------------------------------------------
//   rchar.rs
//
//   Copyright (C) 2020 Andrew Moe
//
//   This program is free software; you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation; either version 2 of the License, or
//   (at your option) any later version.
//
//   This program is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License along
//   with this program; if not, write to the Free Software Foundation, Inc.,
//   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. Or, see
//   <http://www.gnu.org/licenses/gpl-2.0.html>.
// -----------------------------------------------------------------------------

extern crate argparse;
extern crate rand;

use std::char;
use std::process;

use argparse::{ArgumentParser, StoreTrue, Store};
use rand::Rng;
use rand::seq::IteratorRandom;
use rand_regex::Regex;

const OP_CHARSCOPE:u8 = 1;
const OP_REGEX:u8 = 2;
const OP_ALPHANUM:u8 = 4;
const OP_PRINTABLE:u8 = 8;
const OP_ALLASCII:u8 = 16;

fn range2charscope(lobound:u32, hibound:u32) -> String
{
    // TODO: figure out what to do with bad unwraps
    (lobound..hibound).map(|x| char::from_u32(x).unwrap()).collect::<String>()
}

fn generate_string_from_charscope(rng: &mut impl rand::Rng,
                                  length: usize,
                                  charscope: String,
                                  randstr: &mut String)
{
    for _ in 0..length
    {
        // TODO: figure out what to do with bad unwraps
        randstr.push(charscope.chars().choose(rng).unwrap());
    }
}

fn generate_string_from_regex(rng: &mut impl rand::Rng,
                              length: usize,
                              randex: String,
                              randstr: &mut String)
{
    // TODO: figure out what to do with bad unwraps
    let gen = Regex::compile(randex.as_str(), length as u32).unwrap();
    let samples = rng.sample_iter(&gen).take(1).collect::<Vec<String>>();
    randstr.push_str(samples.get(0).unwrap());
}

fn main()
{
    // Define argument/parameters
    let mut arg_length_or_maxrepeat = 8;
    let mut opt_alphanum = false;
    let mut opt_printable = false;
    let mut opt_all = false;
    let mut opt_charscope = "".to_string();
    let mut opt_regex = "".to_string();
    let mut opt_verbose = false;

    let mut rng = rand::thread_rng();
    let mut buf;

    let mut opmode: u8 = 0;
    let mut exitcode: i32 = 0;

    // Parse arguments
    {
        let mut parser = ArgumentParser::new();
        parser.set_description("A handy tool to generate (pseudo-)random strings.");
        parser.refer(&mut arg_length_or_maxrepeat)
            .add_argument("length | maxrepeat", Store,
            "The quantity (length) of characters of which to generate. Or, the maximum \
            amount of characters to repeat (maxrepeat) on unbounded regex quantifiers \
            (e.g. `x*`, `x+` and `x{n,}`). If the regex expression is explicitly bounded, then \
            this argument is ignored. (Tip: regex='a{4,}' maxrepeat=100 will generate a \
            string between 4 and 104 characters long). (Default: 8)");
        parser.refer(&mut opt_all)
            .add_option(&["-A", "--all"], StoreTrue,
            "Generate from all ASCII characters.");
        parser.refer(&mut opt_printable)
            .add_option(&["-P", "--printable"], StoreTrue,
            "Generate from only printable ASCII characters. (Default: True)");
        parser.refer(&mut opt_alphanum)
            .add_option(&["-N", "--alphanum"], StoreTrue,
            "Generate from only alpha-numeric ASCII characters.");
        parser.refer(&mut opt_regex)
            .add_option(&["-r", "--regex"], Store,
            "A regex-like expression from which to generate random UTF-8 characters. An \
            error is thrown if statement contains anchors (`^`, `$`, `\\A`, `\\z`) or word \
            boundary assertions (`\\b`, `\\B`).");
        parser.refer(&mut opt_charscope)
            .add_option(&["-c", "--charscope"], Store,
            "A token of characters from which to randomly select.");
        parser.refer(&mut opt_verbose)
            .add_option(&["-v", "--verbose"], StoreTrue,
            "Display rchar.py debug output during runtime.");
        parser.parse_args_or_exit();
    }

    // Set the program operation mode
    // NOTE: (This will make mode selecting A LOT easier than using
    // an if/else on combinations of boolean values.
    opmode = opmode | (((opt_charscope.len() > 0) as u8) * OP_CHARSCOPE);
    opmode = opmode | (((opt_regex.len() > 0) as u8) * OP_REGEX);
    opmode = opmode | (opt_alphanum as u8 * OP_ALPHANUM);
    opmode = opmode | (opt_printable as u8 * OP_PRINTABLE);
    opmode = opmode | (opt_all as u8) * OP_ALLASCII;

    // Print the input argument for debugging
    if opt_verbose
    {
        eprintln!("debug: rchar length|maxrepeat={}, alphanum={}, printable={}, all={}, \
        charscope=\'{}\', regex=\'{}\', verbose={}", arg_length_or_maxrepeat, opt_alphanum,
                  opt_printable, opt_all, opt_charscope, opt_regex, opt_verbose);
        eprintln!("debug: opmode={}", opmode);
    }

    // Allocate a buffer of the requested size
    buf = String::with_capacity(arg_length_or_maxrepeat);

    // Generate the random string based on the operation mode.
    match opmode
    {
        OP_CHARSCOPE => generate_string_from_charscope(&mut rng, arg_length_or_maxrepeat,
                                                       opt_charscope,&mut buf),

        OP_REGEX => generate_string_from_regex(&mut rng, arg_length_or_maxrepeat,
                                               opt_regex, &mut buf),

        OP_ALPHANUM => generate_string_from_charscope(&mut rng, arg_length_or_maxrepeat,
                                                      format!("{}{}{}",
                                                              range2charscope(65,
                                                                              91),
                                                              range2charscope(97,
                                                                              123),
                                                              range2charscope(48,
                                                                              58)),
                                                      &mut buf),
        // default option
        OP_PRINTABLE | 0 => generate_string_from_charscope(&mut rng, arg_length_or_maxrepeat,
                                                           format!("{}{}",
                                                               range2charscope(32,
                                                                               127),
                                                               range2charscope(128,
                                                                               256)),
                                                           &mut buf),

        OP_ALLASCII => generate_string_from_charscope(&mut rng, arg_length_or_maxrepeat,
                                                      format!("{}",
                                                              range2charscope(0,
                                                                              256)),
                                                      &mut buf),
        _ => {
            eprintln!("Invalid selection of options!");
            exitcode = 1;
        }
    }

    // Print the randomly-generate string to STDOUT
    println!("{}", buf);

    // Exit program with code
    process::exit(exitcode);
}