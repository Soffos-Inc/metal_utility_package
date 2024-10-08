from ._base import ServiceRequestSession
from typing import List, Union, Dict


class DocumentsService(ServiceRequestSession):
    name = 'metal-service-documents'

    def ingest_document(
        self,
        text: str,
        client_id: str,
        document_id: str,
        name: str,
        meta: dict = None,
        chunk_word_length: int = None,
        sent_overlap: int = 1 
    ):
        """Pre-processes document and stores it to Elasticsearch.

        Args:
            text (str): Document text.
            client_id (str): Client's ID.
            document_id (str): Document's ID. Client must keep track of this ID.
            name (str): Document's name.
            meta (dict, optional): Dictionary with any metadata we wish to tag the document with. Defaults to None.
            chunk_word_length (int, optional): Specify how many words per passage when splitting the document to passages. Defaults to None. Service defaults to 100.
            sent_overlap (int, optional): Specify how many sentences should overlap between adjacent passages. Defaults to 1.

        Returns:
            _type_: json
            success (bool): Whether the task succeeded.
        """
        json = {
            "text": text,
            "client_id": client_id,
            "document_id": document_id,
            "name": name
        }
        if meta:
            json["meta"] = meta
        if chunk_word_length is not None:
            json["chunk_word_length"] = chunk_word_length
        if sent_overlap is not None:
            json["sent_overlap"] = sent_overlap

        return self.request(json=json, path="document/ingest")

    def delete_documents(
        self,
        client_id: str,
        document_ids: List[str]
    ):
        """Deletes documents from Elasticsearch.

        Args:
            client_id (str): Client's ID.
            document_ids (List[str]): List of document IDs to be deleted.
        """

        return self.request(
            json={
                "client_id": client_id,
                "document_ids": document_ids
            },
            path="document/delete"
        )
    
    def retrieve_documents(
        self,
        client_id: str,
        query: Union[str, dict, None],
        document_ids: List[str] = None,
        sparse_top_k: int = None,
        dense_top_k: int = None,
        filters: Dict[str, Union[Dict, List, str, int, float, bool]] = None,
        date_from: str = None,
        date_until: str = None
    ):
        #TODO: Add reference to the querying syntax (filters).
        """Retrieves document passages from Elasticsearch with either keyword search, semantic search or both.

        Args:
            client_id (str): Client's ID.
            query (Union[str, dict, None]): Query could be either a string or a dictionary containing the "cleaned_message" field as it is the output of the Query Parser service. It can also be None in the case of simple filtering. More validations happend on the service and instructions are given in the case of invalid combination of parameters. Defaults to None.
            document_ids (List[str], optional): The IDs of the documents we wish to search. Defaults to None.
            sparse_top_k (int, optional): Number of maximum passages retrieved with keyword search. Defaults to None.
            dense_top_k (int, optional): Number of maximum passages retrieved with embedding search. Defaults to None.
            filters (Dict[str, Union[Dict, List, str, int, float, bool]], optional): Additional filters. Defaults to None.
            date_from (Union[str, datetime], optional): Filter documents to those that have been ingested from this date onward. Defaults to None.
            date_until (Union[str, datetime], optional): Filter documents to thost that have been ingested before this date. Defaults to None.

        Returns:
            _type_: List[str]
        """

        json = {
            "query": query,
            "client_id": client_id
        }

        if document_ids is not None:
            json["document_ids"] = document_ids
        if sparse_top_k is not None:
            json["sparse_top_k"] = sparse_top_k
        if dense_top_k is not None:
            json["dense_top_k"] = dense_top_k
        if filters is not None:
            json["filters"] = filters
        if date_from is not None:
            json["date_from"] = date_from
        if date_until is not None:
            json["date_until"] = date_until

        return self.request(json=json, path="document/retrieve")

    def ingest_question(
        self,
        question: Union[str, dict],
        client_id: str,
        document_ids: List[str],
        question_id: str,
        answer: str,
        no_answer: bool,
        from_previous: bool,
        session_id: str = None,
        meta: dict = None
    ):
        """Stores the question, its prediction and all relevant metadata produced during the call.

        Args:
            question (Union[str, dict]): Question string or parsed question dictionary as it comes out of the Query Parser.
            client_id (str): Client's ID.
            document_ids (List[str]): List of document IDs this question was asked upon.
            question_id (str): Question ID.
            answer (str): The answer.
            no_answer (bool): Whether the response isn't really an answer to the question, but a generic response.
            from_previous (bool): Whether the answer was retrieved from previously asked questions.
            meta (dict, optional): Any metadata we wish to tag this question with. Defaults to None.

        Returns:
            _type_: json
            success (bool): Whether the task succeeded.
        """

        json = {
            "question": question,
            "client_id": client_id,
            "document_ids": document_ids,
            "question_id": question_id,
            "answer": answer,
            "no_answer": no_answer,
            "from_previous": from_previous
        }
        if session_id is not None:
            json["session_id"] = session_id
        if meta is not None:
            json["meta"] = meta

        return self.request(json=json, path="question/ingest")

    def delete_questions(
        self,
        client_id: str,
        question_ids: List[str],
        date_from: str = None,
        date_until: str = None
    ):
        """Deletes stored questions and their metadata form Elasticsearch. The question_ids are an intentional requirement, even though we could delete all the client's questions using client_id, to avoid accidentally deleting them all.

        Args:
            client_id (str): Client's ID.
            question_ids (List[str]): List of question IDs.
            date_from (Union[str, datetime], optional): Delete questions that have been indexed from this date onward. This contradicts the fact that we delete by ID, but will be useful when we implement more flexible filtering. Defaults to None.
            date_until (Union[str, datetime], optional): Delete questions that have been indexed before this date. This contradicts the fact that we delete by ID, but will be useful when we implement more flexible filtering. Defaults to None.
        """

        json = {
            "client_id": client_id,
            "question_ids": question_ids
        }
        if date_from:
            json["date_from"] = date_from
        if date_until:
            json["date_until"] = date_until

        return self.request(json=json, path="question/delete")

    def retrieve_questions(
        self,
        client_id: str,
        query: Union[str, dict, None],
        document_ids: List[str] = None,
        sparse_top_k: int = None,
        dense_top_k: int = None,
        filters: Dict[str, Union[Dict, List, str, int, float, bool]] = None,
        date_from: str = None,
        date_until: str = None
    ):
        #TODO: Add reference to the querying syntax (filters).
        """Retrieves document passages from Elasticsearch with either keyword search, semantic search or both.

        Args:
            client_id (str): Client's ID.
            query (Union[str, dict, None], optional): Query could be either a string or a dictionary containing the "cleaned_message" field as it is the output of the Query Parser service. It can also be None in the case of simple filtering. More validations happend on the service and instructions are given in the case of invalid combination of parameters. Defaults to None.
            document_ids (List[str], optional): List of the documents that the returned questions should have been asked upon. Defaults to None.
            sparse_top_k (int, optional): Number of maximum questions retrieved with keyword search. Defaults to None.
            dense_top_k (int, optional): Number of maximum questions retrieved with embedding search. Defaults to None.
            filters (Dict[str, Union[Dict, List, str, int, float, bool]], optional): Additional filters. Defaults to None.
            date_from (Union[str, datetime], optional): Filter questions to those that have been asked from this date onward. Defaults to None.
            date_until (Union[str, datetime], optional): Filter questions to those that have been asked before this date. Defaults to None.

        Returns:
            _type_: List[str]
        """
        json = {
            "client_id": client_id,
            "query": query
        }
        if document_ids is not None:
            json["document_ids"] = document_ids
        if sparse_top_k is not None:
            json["sparse_top_k"] = sparse_top_k
        if dense_top_k is not None:
            json["dense_top_k"] = dense_top_k
        if filters is not None:
            json["filters"] = filters
        if date_from is not None:
            json["date_from"] = date_from
        if date_until is not None:
            json["date_until"] = date_until

        return self.request(json=json, path="question/retrieve")

    def ingest_discussion_context(
        self,
        client_id: str,
        session_id: str,
        context: str
    ):
    
        json = {
            "client_id": client_id,
            "session_id": session_id,
            "context": context
        }

        return self.request(json=json, path="discussion/create")

    def ingest_discussion_interaction(
        self,
        client_id: str,
        session_id: str,
        message_id: int,
        query: str,
        response: str
    ):

        json = {
            "client_id": client_id,
            "session_id": session_id,
            "message_id": message_id,
            "query": query,
            "response": response
        }

        return self.request(json=json, path="discussion/interaction/ingest")

    def delete_discussions(
        self,
        client_id: str,
        session_ids: list[str]
    ):

        json = {
            "client_id": client_id,
            "session_ids": session_ids
        }

        return self.request(json=json, path="discussion/delete")
    
    def retrieve_discussions(
        self,
        client_id: str,
        session_ids: list[str] = None
    ):
        
        json = {
            "client_id": client_id
        }

        if session_ids is not None:
            json["session_ids"] = session_ids
            
        return self.request(json=json, path="discussion/retrieve")

    def retrieve_discussion_interactions(
        self,
        client_id: str,
        session_id: str
    ):

        json = {
            "client_id": client_id,
            "session_id": session_id
        }

        return self.request(json=json, path="discussion/interaction/retrieve")
    
    #chat requests

    def ingest_chat_messages(
        self,
        messages: list[dict],
        client_id: str,
        user_id: str,
        session_id: str,
        session_name: str = None
    ):
        
        json = {
            "messages": messages,
            "client_id": client_id,
            "user_id": user_id,
            "session_id": session_id
        }
        if session_name is not None:
            json['session_name'] = session_name

        return self.request(json=json, path="chat/messages/ingest")
    
    def retrieve_chat_messages(
        self,
        client_id: str,
        user_id: str,
        session_id: str = None,
    ):
        
        json = {
            "client_id": client_id,
            "user_id": user_id
        }

        if session_id is not None:
            json["session_id"] = session_id

        return self.request(json=json, path="chat/messages/retrieve")
    
    def delete_chat_messages(
        self,
        client_id: str,
        user_ids: list[str] = None,
        session_ids: list[str] = None,
        message_ids: list[str] = None
    ):
        
        json = {
            "client_id": client_id
        }

        if user_ids is not None:
            json["user_ids"] = user_ids
        if session_ids is not None:
            json["session_ids"] = session_ids
        if message_ids is not None:
            json["message_ids"] = message_ids

        return self.request(json=json, path="chat/messages/delete")
    

    def ingest_table(
        self,
        client_id: str,
        table: list[str],
        name: str,
        description: str
    ):
        
        json = {
            "client_id": client_id,
            "table": table,
            "name": name,
            "description": description
        }

        return self.request(json=json, path="table/ingest")

    def retrieve_tables(
        self,
        client_id: str,
        query: str = None,
        sparse_top_k: int = None,
        dense_top_k: int = None,
        filters: dict = None,
        date_from: str = None,
        date_until: str = None
    ):
        
        json = {
            "client_id": client_id
        }

        if query is not None:
            json['query'] = query
        if sparse_top_k is not None:
            json['sparse_top_k'] = sparse_top_k
        if dense_top_k is not None:
            json['dense_top_k'] = dense_top_k
        if filters is not None:
            json['filters'] = filters
        if date_from is not None:
            json['date_from'] = date_from
        if date_until is not None:
            json['date_until'] = date_until

        return self.request(json=json, path="table/retrieve")
    
    def delete_tables(
        self,
        client_id: str,
        table_ids: list[str] = None,
        filters: dict = None
    ):
        
        json = {
            "client_id": client_id
        }

        if table_ids is not None:
            json['table_ids'] = table_ids
        if filters is not None:
            json['filters'] = filters

        return self.request(json=json, path="table/delete")

    def create_chatbot(
        self,
        client_id: str,
        name: str,
        role: str,
        chatbot_id: str = None
    ):
        
        json = {
            "client_id": client_id,
            "name": name,
            "role": role
        }

        if chatbot_id is not None:
            json["chatbot_id"] = chatbot_id

        return self.request(json=json, path="chatbot/create")
    
    def delete_chatbots(
        self,
        client_id: str,
        chatbot_ids: list[str] = None,
        filters: dict = None
    ):
        
        json = {
            "client_id": client_id
        }

        if chatbot_ids is not None:
            json["chatbot_ids"] = chatbot_ids
        if filters is not None:
            json["filters"] = filters
        
        return self.request(json=json, path="chatbot/delete")
    
    def get_chatbots(
        self,
        client_id: str,
        chatbot_ids: list[str] = None,
        filters: dict = None
    ):
        
        json = {
            "client_id": client_id
        }

        if chatbot_ids is not None:
            json["chatbot_ids"] = chatbot_ids
        if filters is not None:
            json["filters"] = filters
        
        return self.request(json=json, path="chatbot/retrieve")
        
    def ingest_chatbot_messages(
        self,
        messages: list[dict],
        client_id: str,
        user_id: str,
        chatbot_id: str,
        session_id: str,
        session_name: str = None
    ):
        
        json = {
            "messages": messages,
            "client_id": client_id,
            "user_id": user_id,
            "chatbot_id": chatbot_id,
            "session_id": session_id
        }

        if session_name is not None:
            json["session_name"] = session_name

        return self.request(json=json, path="chatbot/messages/ingest")
    
    def delete_chatbot_messages(
        self,
        client_id: str,
        user_ids: list[str] = None,
        session_ids: list[str] = None,
        chatbot_ids: list[str] = None,
        message_ids: list[str] = None
    ):
        
        json = {
            "client_id": client_id
        }

        if user_ids is not None:
            json["user_ids"] = user_ids
        if session_ids is not None:
            json["session_ids"] = session_ids
        if chatbot_ids is not None:
            json["chatbot_ids"] = chatbot_ids
        if message_ids is not None:
            json["message_ids"] = message_ids
        
        return self.request(json=json, path="chatbot/messages/delete")
    
    def get_chatbot_messages(
        self,
        client_id: str,
        chatbot_id: str,
        user_id: str = None,
        session_ids: list[str] = None
    ):
        
        json = {
            "client_id": client_id,
            "chatbot_id": chatbot_id
        }

        if user_id is not None:
            json["user_id"] = user_id
        if session_ids is not None:
            json["session_ids"] = session_ids

        return self.request(json=json, path="chatbot/messages/retrieve")
