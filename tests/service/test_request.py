from unittest import TestCase

from metal.service.request import (
    EmbeddingsModelService,
    NERModelService
)


class RequestTests(TestCase):
    def test_embeddings_model_service(self):
        strs = ['Hello World!']
        response = EmbeddingsModelService().infer(strs)
        self.assertIn('embeddings', response)

    def test_ner_model_service(self):
        text = 'Bob and Jane got married on the 1st of Jan.'
        response = NERModelService().infer(text)
        self.assertIn('named_entities', response)
