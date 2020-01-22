use crate::pmf::PMF;

fn print(v: &Vec<f64>) {
    let mut dist = Vec::new();
    for (idx, coef) in v.iter().enumerate() {
        if coef > &0.0 {
            let string = format!("{:.4}x^{{{}}}", coef, idx);
            dist.push(string);
        }
    }
    let dist = dist.join("+");
    println!("L(x)={}", dist);
}

fn deriv(v: &[f64]) -> Vec<f64> {
    let mut ret: Vec<f64> = Vec::new();
    for (idx, coef) in v.iter().enumerate() {
        if idx > 0 {
            ret.push(*coef * idx as f64);
        }
    }
    return ret;
}

pub fn run() {
    let deriv = deriv(&PMF);
    print(&PMF.to_vec());
    print(&deriv);
}
