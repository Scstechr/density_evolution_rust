use crate::{ACCURACY, KMAX, MAX};
use std::{env, process::exit};

pub fn return_pmf() -> Vec<f64> {
    let args: Vec<String> = env::args().collect();
    let mut vargs: Vec<f64> = Vec::new();
    vargs.push(0.000000);
    vargs.push(0.000000);
    for i in 1..args.len() {
        let num: f64 = args[i].parse().unwrap();
        vargs.push(num);
    }
    let len = vargs.len();
    if len < 21 {
        for _ in len..21 {
            vargs.push(0.000000);
        }
    } else if len > 21 {
        panic!("invalid argument");
    }
    return vargs;
}

fn subs(v: &Vec<f64>, x: f64) -> f64 {
    let mut sum = 0.0;
    for (idx, coef) in v.iter().enumerate() {
        if coef > &0.0 {
            sum += coef * (x).powf(idx as f64);
        }
    }
    return sum;
}

#[allow(dead_code)]
fn print(name: String, v: &Vec<f64>) {
    let mut dist = Vec::new();
    for (idx, coef) in v.iter().enumerate() {
        if coef > &0.0 {
            let string = format!("{:.4}x^{{{}}}", coef, idx);
            dist.push(string);
        }
    }
    let dist = dist.join("+");
    println!("{}={}", name, dist);
}

fn integral(v: &[f64]) -> Vec<f64> {
    let mut ret: Vec<f64> = Vec::new();
    for (idx, coef) in v.iter().enumerate() {
        if idx > 0 {
            ret.push(*coef * idx as f64);
        }
    }
    return ret;
}

// fn binom(n: i32, k: i32) -> i32 {
//     // (c) Knuth
//     (0..n + 1).rev().zip(1..k + 1).fold(1, |mut r, (n, d)| {
//         r *= n;
//         r /= d;
//         r
//     })
// }

fn mul(v: &Vec<f64>, m: &f64) -> Vec<f64> {
    let mut ret: Vec<f64> = Vec::new();
    for coef in v.iter() {
        ret.push(*coef * m);
    }
    return ret;
}

fn factorial(i: i32) -> i32 {
    if i <= 1 {
        1
    } else {
        i * factorial(i - 1)
    }
}

#[allow(non_snake_case)]
fn get_plr(i: i32, Lx: &Vec<f64>, L1: &f64, lx: &Vec<f64>) -> (f64, f64, f64) {
    let mut Rx = Vec::new();
    let g = (i as f64) * ACCURACY;
    let R1 = g * L1;
    for k in 0..KMAX {
        Rx.push(R1.powf(k as f64) * (-1.0 * R1 as f64).exp() / (factorial(k) as f64));
    }
    let rx = mul(&integral(&Rx), &(1.0 / R1));
    let mut p = 1.0;
    for _ in 0..1000 {
        p = 1.0 - subs(&rx, 1.0 - subs(&lx, p));
    }
    let plr = subs(&Lx, p);
    (g, plr, g * (1.0 - plr))
}

#[allow(non_snake_case)]
pub fn run() {
    let Lx = return_pmf();
    // print("L(x)".to_string(), &Lx);
    let L1 = subs(&integral(&Lx), 1.0);
    let lx = mul(&integral(&Lx), &(1.0 / L1));
    let mut tmax = 0.0;
    for i in 1..(1.0 / ACCURACY) as i32 {
        let (g, plr, t) = get_plr(i, &Lx, &L1, &lx);
        if !MAX {
            println!("{:.4},{:.8},{:.8e}", g, t, plr);
        } else {
            if tmax < t {
                tmax = t;
            } else {
                let (g, plr, t) = get_plr(i - 1, &Lx, &L1, &lx);
                println!("{:.4},{:.8},{:.8e}", g, t, plr);
                exit(0);
            }
        }
    }
}
