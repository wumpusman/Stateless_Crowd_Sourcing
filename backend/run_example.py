from db_connection2 import *
from manager import Manager


def setup_meta(session):

    root_sentence= "There is in Boston a monument of the man who discovered anesthesia; many people are aware, in these latter days, " \
                   "that that man didn't discover it at all, but " \
                   "stole the discovery from another man. Is this truth mighty, " \
                   "and will it prevail? Ah no, my hearers, the monument is made of hardy material, but the lie " \
                   "it tells will outlast it a million years. An awkward, feeble, leaky lie is a thing which you ought to make it your unceasing study to avoid; such a lie as that " \
                   "has no more real permanence than an average truth."

    root_prompt = "Rewrite this as though it were written in contemporary english. You should try to keep the same number of sentences, as well " \
                  "as the general placement of nouns, adjectives and other parts of speech. "

    follow_up_prompt_suggestions = "What are some interesting contemporary issues and examples that you can think of where lying has impacted society, or you personally"


    root_prompt_rate = "How well does this text sound like it was written more like in modern times, as well as the overall quality"

    follow_up_prompt_suggestions_rate="Rate how well you feel the examples and issues provided are interesting?"


    end_prompt="Try to rewrite the text below to make it sound better as well as incorporate the suggestions and ideas discussed on the left. Attempt to maintain " \
               "the number of sentences, and general placement of nouns adjectives and other parts of speech.  " #do this twice
    end_prompt_rate="Rate how well the overall text sounds as well as how well it incorporated the suggestions and ideas on the left"



    body_of_task=Content_Result(root_sentence,is_completed=True)
    prompt=Content_Result(root_prompt,is_completed=True)

    sub_process1_setting={"prompt":Content_Result(root_prompt_rate,is_completed=True),
                          "expected_results":1,
                          "content_to_be_requested":3
                          }

    root_process=Process_Rewrite(body_of_task=body_of_task,prompt=prompt,expected_results=1,content_to_be_requested=4,
                                 subprocess_tuple=(Process_Rate,sub_process1_setting))
    session.add(root_process)

    #second task
    contemporary_issues_prompt=Content_Result(follow_up_prompt_suggestions,is_completed=True)
    sub_process2_setting = {"prompt": Content_Result(follow_up_prompt_suggestions_rate, is_completed=True),
                            "expected_results": 2,
                            "content_to_be_requested": 1
                            }


    contemporary_issues=Process_Rewrite(prompt=contemporary_issues_prompt,expected_results=1,content_to_be_requested=4,
                                        subprocess_tuple=(Process_Rate,sub_process2_setting))


    final_output_prompt=Content_Result(end_prompt,is_completed=True)
    sub_process3_setting = {"prompt": Content_Result(end_prompt_rate, is_completed=True),
                            "expected_results": 1,
                            "content_to_be_requested": 3,
                            "context":contemporary_issues.get_final_results()[0]
                            }

    final_outcome_1=Process_Rewrite(prompt=final_output_prompt,body_of_task=root_process.get_final_results()[0],
                                    context=contemporary_issues.get_final_results()[0],expected_results=1,content_to_be_requested=6,
                                    subprocess_tuple=(Process_Rate,sub_process3_setting)
                                    )

    sub_process4_setting = {"prompt": Content_Result(end_prompt_rate, is_completed=True),
                            "expected_results": 1,
                            "content_to_be_requested": 3,
                            "context": contemporary_issues.get_final_results()[0]
                            }
    final_outcome_2 = Process_Rewrite(prompt=final_output_prompt, body_of_task=final_outcome_1.get_final_results()[0],
                                      context=contemporary_issues.get_final_results()[0], expected_results=4,
                                      content_to_be_requested=1,
                                      subprocess_tuple=(Process_Rate, sub_process4_setting)
                                      )


    session.add(contemporary_issues)
    session.add(final_outcome_1)
    session.add(final_outcome_2)
    return final_outcome_2



def setup_example2(session):
    body_of_task = Content_Result("miss you dude. need to fly me there Asap!!! Saw this card and thought of you. How's"
                                  "life there now it's getting colder? not that you hate cold like I do...anyway see you soon!!!"
                                  "Love, your most beautiful, cool, smart, outstanding, smart, sibling", is_completed=True)
    prompt = Content_Result("What are some ways you would modify the text to make it sound like it was coming from an older Grandfather figure? For example"
                            "ways you would change the text, or reference certain material. List your ideas below.", is_completed=True)
    context = Content_Result("This is a letter from a grandfather who hasn't seen their child in a while. The grandfather misses the other one alot. They come from a warm climate", is_completed=True)
    suggestions = Content_Result("", is_completed=True)




    sub_process1_info = {"prompt": Content_Result(
        "Rate how well you feel the SUGGESTIONS provided below could help inform someone trying to rewrite the text to sound like an older grandfather figure",
        is_completed=True),
        "context": context,
        "content_to_be_requested": 3,
        "expected_results": 1
    }

    sub_process2 = {
        "prompt": Content_Result(
            "Rate how well you feel the rewrite of the text sounds more like the text is coming from an older grandfather figure ",
            is_completed=True),
        "context": context,
        "content_to_be_requested": 3,
        "expected_results": 1
    }

    prompt2=Content_Result("Rewrite the text so it sounds more like the text is coming from an older grandfather figure. Use the context and suggestions as aid in informing what you write. ",is_completed=True)
    #suggestions
    first = Process_Rewrite(body_of_task, prompt=prompt, context=context, suggestion=suggestions, expected_results=1,
                            content_to_be_requested=5,
                            subprocess_tuple=(Process_Rate, sub_process1_info))


    #rewrite one
    second = Process_Rewrite(body_of_task, prompt=prompt2, context=context, suggestion=first.get_final_results()[0]
                             , expected_results=1,
                             content_to_be_requested=5, subprocess_tuple=(Process_Rate, sub_process2))


    session.add(first)
    session.add(second)


    return second


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

    setup_meta(session )
    session.commit()
