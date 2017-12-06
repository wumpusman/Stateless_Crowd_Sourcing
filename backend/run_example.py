from db_connection2 import *
from manager import Manager


def setup_example(session):
    body_of_task = Content_Result("I love going skiiing", is_completed=True)
    prompt = Content_Result("Write the following sentences to make them sound more negative", is_completed=True)
    context = Content_Result("I love my life in america", is_completed=True)
    suggestions = Content_Result("Talk about how skiing has made your life in america great", is_completed=True)

    sub_process1_info = {"prompt": Content_Result(
        "Rate how well the revised content sounds more negative, as well as overall better than the original",
        is_completed=True),
        "context": context,
        "content_to_be_requested": 1,
        "expected_results": 1
    }

    first = Process_Rewrite(body_of_task, prompt=prompt, context=context, suggestion=suggestions, expected_results=1, content_to_be_requested=1,
                            subprocess_tuple=(Process_Rate, sub_process1_info))


    second = Process_Rewrite(first.get_final_results()[0], prompt= prompt, context=context, suggestion= None
                             , expected_results=1,
                             content_to_be_requested=1, subprocess_tuple=(Process_Rate, sub_process1_info))

    prompt_suggestion = Content_Result(
        "Provide suggestions on you would change or edit this text to make it sound more negative",
        is_completed=True)
    sub_process_suggestion_info = {
        "prompt": Content_Result(
            "Rate how well you feel the suggestions would make this text sound more negative, and better in general",
            is_completed=True),
        "context": second.get_final_results()[0],
        "content_to_be_requested": 2,
        "expected_results": 1
    }

    third = Process_Text_Manipulation(second.get_final_results()[0], prompt_suggestion, context=None, suggestion=suggestions,
                                      expected_results=1,
                                      content_to_be_requested=2,
                                      subprocess_tuple=(Process_Rate, sub_process_suggestion_info))
    session.add(first)
    session.add(second)
    session.add(third)

    return second
    '''
    manager = Manager(session)
    users = [("joe", 1), ("bob", 2), ("lee", 3)]

    current_view = manager.request_current_task("joe", 1)
    if "state" in current_view:
        if "exit" == current_view["state"]:
            manager.assign_new_content_to_user("joe", 1)

    print manager.update_after_submitting_content(users[0][0], users[0][1], results={"value": "Fuck this"})

    print manager.update_after_submitting_content(users[1][0], users[1][1], results={"value": ""})
    print manager.update_after_submitting_content(users[1][0], users[1][1], results={"value": "This is bullshit"})

    print manager.update_after_submitting_content(users[0][0], users[0][1], results={"value": "fuck you"})
    '''
if __name__ == '__main__':
    conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source_Test")

    meta.drop_all(bind=conn)  # clear everything
    Base.metadata.create_all(conn)

    setup_example(session )
    session.commit()