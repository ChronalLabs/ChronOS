package com.rtigen.service;

import com.rtigen.engine.IntentEngine;
import com.rtigen.engine.RuleEngine;
import com.rtigen.model.RtiDraft;
import com.rtigen.repository.RtiDraftRepository;
import com.rtigen.adapter.pdf.PdfExportService;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Map;

@ExtendWith(MockitoExtension.class)
public class RtiServiceTest {

    @Mock
    private RtiDraftRepository rtiDraftRepository;
    @Mock
    private IntentEngine intentEngine;
    @Mock
    private RuleEngine ruleEngine;
    @Mock
    private PdfExportService pdfExportService;

    @InjectMocks
    private RtiService rtiService;

    @Test
    public void testCreateDraftFromIntent_CleanQuestions() {
        // Arrange
        String input = "I need info";
        String userId = "user1";

        Mockito.when(intentEngine.analyze(input)).thenReturn(Map.of("subject", "Sub", "department", "Dept"));

        // Dirty formatting: mixed numbering, newlines, double newlines, escaped
        // newlines logic
        String dirtyOutput = "1. Question One\n2) Question Two\n- Question Three\\n4. Question Four";
        Mockito.when(intentEngine.generateQuestions(Mockito.anyMap())).thenReturn(dirtyOutput);

        Mockito.when(rtiDraftRepository.save(Mockito.any(RtiDraft.class))).thenAnswer(i -> i.getArguments()[0]);

        // Act
        RtiDraft draft = rtiService.createDraftFromIntent(input, userId);

        // Assert
        List<String> questions = draft.getQuestions();
        Assertions.assertNotNull(questions);
        Assertions.assertEquals(4, questions.size());

        Assertions.assertEquals("Question One", questions.get(0));
        Assertions.assertEquals("Question Two", questions.get(1));
        Assertions.assertEquals("Question Three", questions.get(2));
        Assertions.assertEquals("Question Four", questions.get(3));
    }
}
