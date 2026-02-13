package com.rtigen.adapter.pdf;

import com.rtigen.model.RtiDraft;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.PDPageContentStream;
import org.apache.pdfbox.pdmodel.font.PDType1Font;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.springframework.stereotype.Service;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

@Service
public class PdfExportService {

    public byte[] generateRtiPdf(RtiDraft draft) throws IOException {
        try (PDDocument document = new PDDocument()) {
            PDPage page = new PDPage(PDRectangle.A4);
            document.addPage(page);

            try (PDPageContentStream contentStream = new PDPageContentStream(document, page)) {

                // HEADER
                contentStream.beginText();
                contentStream.setFont(PDType1Font.HELVETICA_BOLD, 16);
                contentStream.newLineAtOffset(50, 750);
                contentStream.showText("Application under Right to Information Act, 2005");
                contentStream.endText();

                int yPosition = 700;
                int margin = 50;

                // TO SECTION
                writeText(contentStream, margin, yPosition, "To,", PDType1Font.HELVETICA, 12);
                yPosition -= 15;
                writeText(contentStream, margin, yPosition, "The Public Information Officer,",
                        PDType1Font.HELVETICA_BOLD, 12);
                yPosition -= 15;
                writeText(contentStream, margin, yPosition,
                        draft.getDepartment() != null ? draft.getDepartment() : "[Department Name]",
                        PDType1Font.HELVETICA, 12);
                yPosition -= 15;
                writeText(contentStream, margin, yPosition, draft.getState() != null ? draft.getState() : "[State]",
                        PDType1Font.HELVETICA, 12);

                yPosition -= 30;

                // APPLICANT DETAILS
                if (draft.getApplicant() != null) {
                    writeText(contentStream, margin, yPosition,
                            "Name of Applicant: "
                                    + (draft.getApplicant().getName() != null ? draft.getApplicant().getName() : ""),
                            PDType1Font.HELVETICA, 12);
                    yPosition -= 15;
                    writeText(contentStream, margin, yPosition, "Address: "
                            + (draft.getApplicant().getAddress() != null ? draft.getApplicant().getAddress() : ""),
                            PDType1Font.HELVETICA, 12);
                    yPosition -= 30;
                }

                yPosition -= 40;

                // SUBJECT
                writeText(contentStream, margin, yPosition, "Subject: " + draft.getSubject(),
                        PDType1Font.HELVETICA_BOLD, 12);
                yPosition -= 30;

                // BODY
                writeText(contentStream, margin, yPosition, "Respected Sir/Madam,", PDType1Font.HELVETICA, 12);
                yPosition -= 20;

                String bodyIntro = "Please provide the following information under the RTI Act, 2005:";
                writeText(contentStream, margin, yPosition, bodyIntro, PDType1Font.HELVETICA, 12);
                yPosition -= 20;

                // QUESTIONS
                if (draft.getQuestions() != null) {
                    int qNum = 1;
                    for (String q : draft.getQuestions()) {
                        writeText(contentStream, margin, yPosition, qNum + ". " + q, PDType1Font.HELVETICA, 12);
                        yPosition -= 20; // Simplified multiline handling for MVP
                        qNum++;
                    }
                }

                yPosition -= 30;
                writeText(contentStream, margin, yPosition, "I am attaching the application fee of Rs. 10/-.",
                        PDType1Font.HELVETICA, 12);

                // SIGNATURE
                yPosition -= 60;
                writeText(contentStream, margin + 350, yPosition, "Sincerely,", PDType1Font.HELVETICA, 12);
                yPosition -= 40;
                if (draft.getApplicant() != null) {
                    writeText(contentStream, margin + 350, yPosition, draft.getApplicant().getName(),
                            PDType1Font.HELVETICA_BOLD, 12);
                }
            }

            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            document.save(baos);
            return baos.toByteArray();
        }
    }

    private void writeText(PDPageContentStream stream, int x, int y, String text,
            org.apache.pdfbox.pdmodel.font.PDFont font, int size) throws IOException {
        if (text == null)
            return;
        stream.beginText();
        stream.setFont(font, size);
        stream.newLineAtOffset(x, y);
        stream.showText(text);
        stream.endText();
    }
}
