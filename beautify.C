#include "TH1D.h"
#include "TFile.h"
#include "TStyle.h"


/*
void beautify() {
    // ---------- 1. OPEN INPUT FILE ----------
    TFile* input = TFile::Open("output0.root");
    if (!input || input->IsZombie()) {
        printf("❌ Error: Cannot open build/output0.root\n");
        return;
    }
    
    // ---------- 2. GET THE HISTOGRAM ----------
    TH1D* h = (TH1D*)input->Get("EdepDecayGammaDaughters");
    if (!h) {
        printf("❌ Error: Cannot find EdepDecayGammaDaughters histogram\n");
        return;
    }
    
    // ---------- 3. CLONE IT (so original is untouched) ----------
    TH1D* h_beauty = (TH1D*)h->Clone("GammaEnergy_beautified");
    
    // ---------- 4. BEAUTIFY IT ----------
    // Colors
    h_beauty->SetLineColor(kBlue);
    h_beauty->SetLineWidth(2);
    h_beauty->SetFillColorAlpha(kBlue, 0.35);
    h_beauty->SetFillStyle(1001);
    
    // Titles
    h_beauty->GetXaxis()->SetTitle("Energy (MeV)");
    h_beauty->GetYaxis()->SetTitle("Counts");
    
    // Title sizes
    h_beauty->GetXaxis()->SetTitleSize(0.05);
    h_beauty->GetYaxis()->SetTitleSize(0.05);
    h_beauty->GetXaxis()->SetLabelSize(0.045);
    h_beauty->GetYaxis()->SetLabelSize(0.045);
    
    // Title offsets
    h_beauty->GetXaxis()->SetTitleOffset(1.1);
    h_beauty->GetYaxis()->SetTitleOffset(1.2);

    
    // Range (optional)
    // h_beauty->GetXaxis()->SetRangeUser(0, 0.8);
    TCanvas* c1 = new TCanvas("c1", "Beautified Histogram", 800, 600);
    c1->SetGrid();
    gPad->SetLogy(1);
    h_beauty->Draw("HIST");
    c1->SaveAs("beautified_histogram_v2.png");
    
    // ---------- 5. SAVE TO OUTPUT FILE ----------
    output->cd();  // CRITICAL: This makes Write() go to beautified.root
    h_beauty->Write("GammaEnergy", TObject::kOverwrite);
    
    // ---------- 6. CLEAN UP ----------
    output->Close();
    input->Close();
    
    printf("✅ Done! Histogram saved to beautified.root\n");
    printf("   Open it with: root beautified.root\n");
    printf("   Then type: GammaEnergy->Draw()\n");
}
    */

    // auto_save_histos.C
void beautify(const char* filename = "output0.root")
{
    // Open the ROOT file
    TFile *file = TFile::Open(filename);
    if (!file || file->IsZombie()) {
        printf("Error: Cannot open file %s\n", filename);
        return;
    }
    
    // Create output directory for plots
    gSystem->mkdir("histogram_plots", kTRUE);
    gStyle->SetOptStat(0);
    
    // Get list of keys in the file
    TList *keys = file->GetListOfKeys();
    TIter next(keys);
    TKey *key;
    
    int counter = 0;
    
    // Loop through all objects in the file
    while ((key = (TKey*)next())) {
        TObject *obj = key->ReadObj();
        
        // Check if it's a histogram
        if (obj->InheritsFrom("TH1") || obj->InheritsFrom("TH2") || obj->InheritsFrom("TH3")) {
            
            TH1 *hist = (TH1*)obj;
            TString histName = hist->GetName();
            TString histTitle = hist->GetTitle();
            
            printf("Processing histogram %d: %s - %s\n", ++counter, histName.Data(), histTitle.Data());
            
            // Create canvas with nice proportions
            TCanvas *c = new TCanvas(histName, histTitle, 800, 600);
            
            // Apply some basic styling
            c->SetLeftMargin(0.12);
            c->SetRightMargin(0.05);
            c->SetBottomMargin(0.12);
            c->SetTopMargin(0.08);
            
            // Set histogram styling
            hist->SetStats(kTRUE);
            hist->SetLineWidth(2);
            hist->SetLineColor(kBlue);
            hist->SetFillColor(38);  // Light blue
            hist->SetFillStyle(1001);
            
            // Draw the histogram
            hist->Draw("HIST");

            hist->GetXaxis()->SetTitle("Energy (MeV)");
            hist->GetYaxis()->SetTitle("Counts");

            gPad->SetLogy(1);  // Set log scale for y-axis
            
            // Save as PNG with histogram name
            TString outputName = TString::Format("histogram_plots/%s.png", histName.Data());
            c->SaveAs(outputName);
            
            // Clean up
            delete c;
        }
    }
    
    file->Close();
    printf("\nDone! Processed %d histograms. Plots saved in 'histogram_plots/' directory.\n", counter);
}