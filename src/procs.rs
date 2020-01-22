use crate::pmf::PMF;

const KMAX: i32 = 15;
const M: i32 = 10000;

fn subs(v: &Vec<f64>, x: f64) -> f64 {
    let mut sum = 0.0;
    for (idx, coef) in v.iter().enumerate() {
        if coef > &0.0 {
            sum += coef * (x).powf(idx as f64);
        }
    }
    return sum;
}

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

fn binom(n: i32, k: i32) -> i32 {
    // (c) Knuth
    (0..n + 1).rev().zip(1..k + 1).fold(1, |mut r, (n, d)| {
        r *= n;
        r /= d;
        r
    })
}

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
pub fn run() {
    let Lx = PMF.to_vec();
    let L1 = subs(&integral(&Lx), 1.0);
    let lx = mul(&integral(&Lx), &(1.0 / L1));
    // print("L(x)".to_string(), &Lx);
    // print("l(x)".to_string(), &lx);
    let tmax = 0.0;
    for i in (0..10000) {
        let mut Rx = Vec::new();
        let g = (i as f64) * 0.0001;
        // println!("G:{}", g);
        let R1 = g * L1;
        // println!("R1:{}", R1);
        for k in 0..KMAX {
            Rx.push(R1.powf(k as f64) * (-1.0 * R1 as f64).exp() / (factorial(k) as f64));
        }
        let rx = mul(&integral(&Rx), &(1.0 / R1));
        // print("R(x)".to_string(), &Rx);
        // print("r(x)".to_string(), &rx);
        let mut p = 1.0;
        for _ in 0..1000 {
            p = 1.0 - subs(&rx, 1.0 - subs(&lx, p));
        }
        let plr = subs(&Lx, p);
        println!("{:.4},{:.8},{:.8e}", g, g * (1.0 - plr), plr);
    }
    // }
}
