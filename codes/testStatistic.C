//{
//TF1* f = new TF1("f","(1/(2*TMath::Sqrt(x)) * (1/(2*TMath::Pi())) * (TMath::Exp(-0.5*pow(TMath::Sqrt(x)+([0]-[1])/1., 2)) + TMath::Exp(-0.5*pow(TMath::Sqrt(x)-([0]-[1])/1., 2))) )",0,10);
//f->SetParameters(1, 1);
//f->Draw();
//
//f->SetParameters(1, 2);
//f->Draw("same");
//}

#include "TString.h"

Double_t f_pdf(Double_t *x, Double_t *par){
  Float_t xx =x[0];
  Double_t f = (1/(2*sqrt(xx))) * (1/(2*TMath::Pi())) * (TMath::Exp(-0.5*pow(sqrt(xx)+(par[0]-par[1])/pow(par[2], 2), 2)) + TMath::Exp(-0.5*pow(sqrt(xx)-(par[0]-par[1])/pow(par[2], 2), 2)));
  return f;
}

void testStatistic(){

  gROOT->SetStyle("ATLAS");
  gStyle->SetStatStyle(0); 
  gStyle->SetTitleStyle(0); 

  gROOT->ForceStyle();

  TCanvas *canvas = new TCanvas("canvas");
  canvas->cd();


  float minX = 1;
  float maxX = 30;
  float sigma = 0.55;

  float qObserved = 8.;

  TH2F *hframe = new TH2F("hframe", "hframe", 1, minX, maxX, 1, 5e-5, 1.);
  hframe->GetXaxis()->SetTitle("q_{1}");
  hframe->Draw();

  gPad->SetLogy();

  TF1 *f0 = new TF1("f0_pdf",f_pdf,minX,maxX,3);
  f0->SetParameters(1,1,sigma);
  f0->SetParNames("mu","mu_prime","sigma");
  f0->Draw("same");

  TF1 *f1 = new TF1("f1_pdf",f_pdf,minX,maxX,3);
  f1->SetParameters(1,0,sigma);
  f1->SetParNames("mu","mu_prime","sigma");
  f1->SetLineColor(kRed);
  f1->Draw("same");

  TLine *obsLine = new TLine(qObserved, 5e-5, qObserved, 0.6);
  obsLine->SetLineStyle(2);
  obsLine->SetLineWidth(2);
  obsLine->SetLineColor(kBlue);
  obsLine->Draw("same");

  f0_painted = new TF1("f0_pdf_painted",f_pdf,qObserved,maxX,3);
  f0_painted->SetParameters(0,0,sigma);
  f0_painted->SetParNames("mu","mu_prime","sigma");
  f0_painted->SetFillStyle(1001);
  f0_painted->SetFillColor(kGreen);
  f0_painted->Draw("FCsame");

  f1_painted = new TF1("f1_pdf_painted",f_pdf,minX,qObserved,3);
  f1_painted->SetParameters(0,1,sigma);
  f1_painted->SetParNames("mu","mu_prime","sigma");
  f1_painted->SetLineColor(kRed);
  f1_painted->SetFillStyle(1001);
  f1_painted->SetFillColor(kYellow);
  f1_painted->Draw("FCsame");

  f0->Draw("same");
  obsLine->Draw("same");

  TLegend *legend = new TLegend(0.7, 0.75, 0.90, 0.90);
  legend->SetBorderSize(0); 
  legend->SetTextSize( 0.035 );
  legend->SetTextFont( 42 );
  legend->SetFillColor( 0 );
  legend->SetFillStyle(1001);
  legend->AddEntry(f0, "H_{0}: f(q_{#mu=1}|1)", "l");
  legend->AddEntry(f1, "H_{1}: f(q_{#mu=1}|0)", "l");
  legend->Draw();

  TLatex latex;
  int colorRed = kRed;
  int colorBlue = kBlue;
  latex.SetTextSize(0.035);
  latex.SetTextAlign(13);  //align at top
  latex.DrawLatex(qObserved+3, 1e-3, Form("p_{s+b}=%.2e", f0_painted->Integral(qObserved, maxX)));
  latex.DrawLatex(qObserved-4.5, 7e-2, Form("#color[%d]{p_{b}=%.2e}"  , colorRed, f1_painted->Integral(minX, qObserved)));
  latex.DrawLatex(qObserved+1, 3e-1, Form("#color[%d]{CL_{s} = #frac{CL_{s+b}}{CL_{b}} = %.2e}"  , colorBlue, f0_painted->Integral(qObserved, maxX)/(1-f1_painted->Integral(minX, qObserved))));
  latex.DrawLatex(qObserved, 3e-5, Form("#color[%d]{q_{1, obs}}" ));

  TArrow *ar = new TArrow();
  ar->SetLineWidth(2);
  ar->SetLineColor(kRed);
  ar->SetFillColor(kRed);
  ar->DrawArrow(6., 0.0454, 7., 0.00463, 0.02, "|>");

  TArrow *ar2 = new TArrow();
  ar2->SetLineWidth(2);
  ar2->SetLineColor(kBlack);
  ar2->SetFillColor(kBlack);
  ar2->DrawArrow(12.62, 0.0005987, 10.813, 0.0001185, 0.02, "|>");

  TLatex *myLabel = new TLatex();
  myLabel->SetNDC();
  myLabel->SetTextFont(72);
  myLabel->SetTextColor(kBlack);
  myLabel->DrawLatex(0.55, 0.2, "R. Caminal - PhD Thesis");

  canvas->Print("pdfTestHypothesisExample.eps");

}
