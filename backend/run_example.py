from db_connection2 import *
from manager import Manager
import re
import os
def setup_summary(session):
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    dir_path = os.path.join(dir_path, "little_match_girl")
    little_match_girl = open(dir_path,"rb")
    little_match_girl_text=little_match_girl.read()
    little_match_girl.close()
    little_match_girl=little_match_girl_text

    as_arry=re.split("[.;?]", little_match_girl)
    #as_arry=as_arry[0:len(as_arry)/2]
    match_girl_batch_size_5=[]
    for i in xrange(0,len(as_arry),5):
        match_girl_batch_size_5.append(".".join(as_arry[i:i+5]))

    recurse_summary(session,match_girl_batch_size_5,0)

def _merge_step(session,left_content_result,right_content_result):
    default_sub_process_amount = 5
    default_process_amount = 4

    merge_prompt="The text below and the text to left are two related parts of a story. Please combine them into a single summary."

    merge_rate="Looking at the text BELOW and the text on the LEFT, please rate how well 'content to be evaluate' incorporates them both " \
               "into a single summary"

    cr_prompt=Content_Result(merge_prompt,is_completed=True)
    cr_prompt_rate=Content_Result(merge_rate,is_completed=True)

    sub_process = {"prompt": cr_prompt_rate,
                   "expected_results": 1,
                   "context":right_content_result,
                   "content_to_be_requested": default_sub_process_amount}

    merge_process = Process_Rewrite(body_of_task=left_content_result, context=right_content_result, prompt=cr_prompt,
                                      expected_results=1, content_to_be_requested=default_process_amount,
                                    subprocess_tuple=(Process_Rate,sub_process))
    session.add(merge_process)
    session.commit()
    return merge_process

def _summary_step(session,content):
    default_sub_process_amount=1
    default_process_amount=1
    summary_prompt="For the text below, to the best to your ability, " \
                   "please write a concise summary that incorporates the keys points and events of the text below"

    summary_rate_prompt="The 'content to be evaluated' is intended to be a summary of the text below. " \
                        "Rate how well you feel it accurately captures the full meaning and key events. "

    cr_prompt=Content_Result(summary_prompt,is_completed=True)
    cr_prompt_rate=Content_Result(summary_rate_prompt,is_completed=True)

    body_content = None
    if type(content) == type(""):
        body_content=Content_Result(content,is_completed=True)
    else:
        body_content=content

    sub_process = {"prompt": cr_prompt_rate,
                        "expected_results": 1,
                        "content_to_be_requested": default_sub_process_amount}

    summary_process=Process_Rewrite(body_of_task=body_content,prompt=cr_prompt,
                                    expected_results=1,content_to_be_requested=default_process_amount,
                                    subprocess_tuple=(Process_Rate, sub_process))
    session.add(summary_process)
    session.commit()
    return summary_process


def recurse_summary(session,text_block_ary, depth):
   # print len(text_block_ary)
    sub_group_len=len(text_block_ary)/2

    if sub_group_len==0:

        return _summary_step(session,text_block_ary[0])


    left= text_block_ary[:sub_group_len]
    right= text_block_ary[sub_group_len:]

    left_process=recurse_summary(session,left,depth+1)
    right_process=recurse_summary(session,right,depth+1)

    merge_process=_merge_step(session,left_process.get_final_results()[0],right_process.get_final_results()[0])
    #if right Node is empty  just return left Node (summariazation)
    #create B =(merge process of left and right)
    #create C = summaziation (B)
    #return C
    #print left_node+right_node
    return merge_process

    '''
    recurse left, recurse right

    if sub_group_len/2 ==0 return

    '''


def setup_narrative_plot(session):

    default_rewrite_amount = 1
    default_sub_process_amount = 3

    root_body="The two detectives arrived backstage and saw the actor's body lying on the floor."
    root_prompt="Looking at the brief description of this scene what are some questions you would ask " \
                "the writer to have a better sense of what the story is about"

    answer_followup="Looking at the brief description of the story, try to provide an answer to the question that you " \
                  "think would make the story more interesting. Briefly explain why"

    merge_answer_to_body="Incorporate the information described on the left into the description of the scene below"

    next_step = "given the description of the plot below, what should happen next"

    rate_root="Rate how well the questions listed below would help clarify what the story is about"
    rate_answer_followup="Rate how well you feel the answer would address the question and make the 'context' for the story below" \
                         " more engaging"
    rate_merge_answer_to_body="Rate how well you feel the text below is incorporated into the content "
    rate_next_step="Given the background of the story, rate how well the text below would aid the story"

    cr_root_prompt = Content_Result(root_prompt, is_completed=True)
    cr_root_body = Content_Result(root_body, is_completed=True)
    cr_plot_answer_prompt = Content_Result(answer_followup, is_completed=True)
    cr_merge_plot_prompt = Content_Result(merge_answer_to_body, is_completed=True)


    ####
    sub_root_process = {"prompt": Content_Result(rate_root, is_completed=True),
                        "expected_results": 1,
                        "context":cr_root_body,
                        "content_to_be_requested": default_sub_process_amount}

    root_process=Process_Rewrite(body_of_task=cr_root_body, prompt=cr_root_prompt,
                                   expected_results=1,
                                   content_to_be_requested=5,
                                   subprocess_tuple=(Process_Rate, sub_root_process)
                                   )
    ####
    sub_answer_process={"prompt": Content_Result(rate_answer_followup, is_completed=True),
                        "expected_results": 1,

                        "content_to_be_requested": default_sub_process_amount}

    answer_process=Process_Rewrite(body_of_task=root_process.get_final_results()[0], prompt=cr_plot_answer_prompt,
                                   context=cr_root_body,
                                   expected_results=1,
                                   content_to_be_requested=5,
                                   subprocess_tuple=(Process_Rate, sub_answer_process)
                                   )

    #rate_merge_answer_to_body
    sub_merge_process = {"prompt": Content_Result(rate_merge_answer_to_body, is_completed=True),
                          "expected_results": 1,
                          "content_to_be_requested": default_sub_process_amount}


    merge_process = Process_Rewrite(body_of_task=cr_root_body, prompt=cr_merge_plot_prompt,
                                 context=answer_process.get_final_results()[0] ,
                                 expected_results=1,
                                 content_to_be_requested=4,
                                 subprocess_tuple=(Process_Rate, sub_merge_process)
                                 )




    ####
    sub_loop_process = {"prompt": Content_Result(rate_root, is_completed=True),
                        "expected_results": 1,

                        "content_to_be_requested": default_sub_process_amount}

    root_loop_process=Process_Rewrite(body_of_task=merge_process.get_final_results()[0], prompt=cr_root_prompt,
                                   expected_results=1,
                                   content_to_be_requested=5,
                                   subprocess_tuple=(Process_Rate, sub_loop_process)
                                   )
    ####
    sub_answer_process2={"prompt": Content_Result(rate_answer_followup, is_completed=True),
                        "expected_results": 1,
                        "context":merge_process.get_final_results()[0],
                        "content_to_be_requested": default_sub_process_amount}

    answer_process2=Process_Rewrite(body_of_task=root_loop_process.get_final_results()[0], prompt=cr_plot_answer_prompt,
                                   context=merge_process.get_final_results()[0],
                                   expected_results=1,
                                   content_to_be_requested=5,
                                   subprocess_tuple=(Process_Rate, sub_answer_process2)
                                   )

    sub_merge_process2 = {"prompt": Content_Result(rate_merge_answer_to_body, is_completed=True),
                          "expected_results": 1,

                          "content_to_be_requested": default_sub_process_amount}


    merge_process2 = Process_Rewrite(body_of_task=merge_process.get_final_results()[0], prompt=cr_merge_plot_prompt,
                                 context=answer_process2.get_final_results()[0] ,
                                 expected_results=1,
                                 content_to_be_requested=5,
                                 subprocess_tuple=(Process_Rate, sub_merge_process2)
                                 )



    session.add(root_process)
    session.add(answer_process)
    session.add(merge_process)
    session.add(root_loop_process)
    session.add(answer_process2)
    session.add(merge_process2)


def setup_business_advice(session):


    default_rewrite_amount = 1
    default_sub_process_amount = 3

    root_body="I work for a small business that provides home health care. As you can imagine, I depend on my vehicle to get to my clients' homes." \
              "My care recently broke down and is goign to cost me about $600. I've turned everywhere. The bank, credit cards, installment loans, family" \
              "friends, etc. all have been denied. I have nowhere else to turn and I'm running out of options and money. I'm depending on my friend's" \
              "car to get to work but that option is running low as well. Am I in a position to ask my manager (owner of the company) for an advance to help" \
              "me pay for the repairs"
    root_prompt = "To the best of your ability summarize what the situation and problem this person is having."

    followup_prompt = "Write some advice with a bit of detail for what the person should do"

    followup_prompt2="Rewrite the the following text to incorporate the ideas and content shown in the 'context' bar. Try to keep the style and flow of the text as best, but it should sound coherent and use the information in 'context'"
    followup_body2="if you're the one person with a job that signals that you start with , then you should be able to do all done well"


    root_prompt_rate = "Rate how well the meaning of the text was captured"
    prompt_followup_rate = "Rate how well the text handles the issue or question"
    prompt_followup2_rate = "Rate how well the the text incorporates the style of the text below and the content of 'context'"





    cr_root_prompt = Content_Result(root_prompt, is_completed=True)
    cr_root_body = Content_Result(root_body, is_completed=True)

    cr_followup_prompt = Content_Result(followup_prompt, is_completed=True)
    cr_followup_prompt2 = Content_Result(followup_prompt2, is_completed=True)
    cr_followup_body2=Content_Result(followup_body2,is_completed=True)

    sub_root_process = {"prompt": Content_Result(root_prompt_rate, is_completed=True),
                        "expected_results": 1,
                        "content_to_be_requested": default_sub_process_amount}


    root_process = Process_Rewrite(body_of_task=cr_root_body, prompt=cr_root_prompt,
                                   expected_results=1,
                                   content_to_be_requested=4,
                                   subprocess_tuple=(Process_Rate, sub_root_process)
                                   )

    sub_f_process = {"prompt": Content_Result(prompt_followup_rate, is_completed=True),
                     "expected_results": 1,
                     "content_to_be_requested": default_sub_process_amount}

    followup_process = Process_Rewrite(body_of_task=root_process.get_final_results()[0],
                                       prompt=cr_followup_prompt,
                                       expected_results=1,
                                       content_to_be_requested=4,
                                       subprocess_tuple=(Process_Rate, sub_f_process))

    sub_f2_process = {"prompt": Content_Result(prompt_followup2_rate, is_completed=True),
                      "expected_results": 1,
                      "context": followup_process.get_final_results()[0],
                      "content_to_be_requested": default_sub_process_amount}

    followup_process2 = Process_Rewrite(body_of_task=cr_followup_body2,
                                        context=followup_process.get_final_results()[0], prompt=cr_followup_prompt2,
                                        expected_results=1,
                                        content_to_be_requested=4,
                                        subprocess_tuple=(Process_Rate, sub_f2_process)
                                        )

    session.add(root_process)
    session.add(followup_process)
    session.add(followup_process2)

def setup_life_advice(session):
    '''
      My 'adult' 23-year-old son is home for the holidays. He leads a more liberal lifestyle than my husband and me, and suffice it to say not only do our politics not match up, but neither do our hygiene practices. To be blunt, his body order is killing us! I didn't raise him this way and I absolutely can't stand it. I just can't embrace not showering daily and not using a daily dose of antiperspirant. How do you address an awkward and difficult topic with a person who is also awkward and difficult?

      List a couple (3-4 ideas) as to how handle answering this question in a way that is considerate and sensitive, but also deals with the problem. Provide an explanation as to how they would help.

     Using the suggestions and ideas on the left, write a response to the problem above attempting to be sensitive and sincere to the issue.

     Try to keep the style (but not the content), and incorporate the ideas and content described on the left to the best of your ability.
     '''

    root_prompt = "List a couple (3-4 ideas) as to how to answer this in a way that is also considerate and sensitive, provide a brief explanation as to how they would help."


    root_body = "My 'adult' 23-year-old son is home for the holidays. He leads a more liberal lifestyle than my husband and me, and suffice it to say not only do our politics not match up, but neither do our hygiene practices. " \
                "To be blunt, his body order is killing us! " \
                "I didn't raise him this way and I absolutely can't stand it. " \
                "I just can't embrace not showering daily and not using a daily dose of antiperspirant. " \
                "How do you address an awkward and difficult topic with a person who is also awkward, sensitive and difficult?"

    followup_prompt = "Using the suggestions and ideas on the left, write a response to the problem above attempting to be sensitive and sincere to the issue."

    followup_prompt2 = "Using the suggestions and context on the left, rewrite the text below to incorporate that content (keep the style of this letter but make the content fit the suggestions and CONTEXT on the left)"
    followup_body2="This year, you grew to be taller than me. I didn't know that would happen so soon. " \
                   "I have such mixed feelings about the man you are becoming. I am so proud of you for being smart and loving and courageous. " \
                   "But I'm not ready for you to be so grown up already." \
                   " I see the little boys wearing clothes that you wore not so long ago and I remember you as a small child. "

    default_rewrite_amount = 1
    default_sub_process_amount =3

    cr_root_prompt = Content_Result(root_prompt, is_completed=True)
    cr_root_body = Content_Result(root_body, is_completed=True)

    cr_followup_prompt = Content_Result(followup_prompt, is_completed=True)
    cr_followup_prompt2 = Content_Result(followup_prompt2, is_completed=True)
    cr_followup_body2=Content_Result(followup_body2,is_completed=True)
    # body_of_task=None,prompt=None,suggestion=None,context=None, displayed_result=None, expected_results=1, content_to_be_requested=3, subprocess_tuple=None

    root_prompt_rate = "Rate how well the ideas listed below would improve the content"
    prompt_followup_rate = "Rate how well the text below improves and expands the content. Uses the suggestions and context to help inform you"
    prompt_followup2_rate = "Rate how well the the text below better matches the suggestions and concepts written and described on the left"





    sub_root_process = {"prompt": Content_Result(root_prompt_rate, is_completed=True),
                        "expected_results": 1,
                        "content_to_be_requested": default_sub_process_amount}
    root_process = Process_Rewrite(body_of_task=cr_root_body, prompt=cr_root_prompt,
                                   expected_results=1,
                                   content_to_be_requested=4,
                                   subprocess_tuple=(Process_Rate, sub_root_process)
                                   )

    sub_f_process = {"prompt": Content_Result(prompt_followup_rate, is_completed=True),
                     "expected_results": 1,
                     "suggestion":root_process.get_final_results()[0],
                     "content_to_be_requested": default_sub_process_amount}
    followup_process = Process_Rewrite(body_of_task=cr_root_body, suggestion=root_process.get_final_results()[0],
                                       prompt=cr_followup_prompt,
                                       expected_results=1,
                                       content_to_be_requested=4,
                                       subprocess_tuple=(Process_Rate, sub_f_process))


    sub_f2_process = {"prompt": Content_Result(prompt_followup2_rate, is_completed=True),
                      "expected_results": 1,
                      "context":followup_process.get_final_results()[0],
                      "suggestion":root_process.get_final_results()[0],
                      "content_to_be_requested": default_sub_process_amount}

    followup_process2 = Process_Rewrite(body_of_task=cr_followup_body2,suggestion=root_process.get_final_results()[0], context=followup_process.get_final_results()[0], prompt=cr_followup_prompt2,
                                        expected_results=1,
                                        content_to_be_requested=4,
                                        subprocess_tuple=(Process_Rate, sub_f2_process)
                                        )


    session.add(root_process)
    session.add(followup_process)
    session.add(followup_process2)
    session.commit()
def setup_multiple_tasks(session):
        setup_business_advice(session)
        setup_life_advice(session)


        root_prompt="List 3 or 4 ideas and suggestions that one could add, edit or change to make this a better happy birthday letter. My dad wrote an incredibly short disheartening " \
                    "letter and I was wondering of any ideas how he could have improved it "
        root_body="sorry about that so Happy 30th. No longer a millennial and what does it make you. love, dad "
        root_context="I just turned 30 and was feeling pretty existential, in response my dad forgot my birthday and wrote this incredibly short letter/card."

        followup_prompt="Using the ideas on the left, try to extend and improve this  birthday letter. Basically use the ideas on the left to help make this a longer, better " \
                        "and sweeter card. My dad wrote a very meh birthday letter "

        followup_prompt2="List 3 or 4 ideas and suggestions to improve, edit, and expand this birthday card my dad wrote to make it sound better "

        followup_prompt3=""+followup_prompt

        default_rewrite_amount = 1
        default_sub_process_amount = 3

        cr_root_prompt = Content_Result(root_prompt, is_completed=True)
        cr_root_body=Content_Result(root_body,is_completed=True)
        cr_root_context= Content_Result(root_context, is_completed=True)
        cr_followup_prompt = Content_Result(followup_prompt, is_completed=True)
        cr_followup_prompt2= Content_Result(followup_prompt2, is_completed=True)
        cr_followup_prompt3 = Content_Result(followup_prompt3, is_completed=True)
        #body_of_task=None,prompt=None,suggestion=None,context=None, displayed_result=None, expected_results=1, content_to_be_requested=3, subprocess_tuple=None

        root_prompt_rate="Rate how well the ideas listed below would improve the content"
        prompt_followup_rate="Rate how well the text below improves and expands the content. Uses the suggestions and context to help inform you"
        prompt_followup2_rate="Rate how well the ideas listed below would improve the content"
        prompt_followup3_rate="Rate how well the text below improves and expands the content. Uses the suggestions and context to help inform you"

        sub_root_process={"prompt":Content_Result(root_prompt_rate,is_completed=True),
                          "context":cr_root_context,
                          "expected_results":1,
                          "content_to_be_requested":default_sub_process_amount}
        sub_f_process={"prompt":Content_Result(prompt_followup_rate,is_completed=True),
                          "context":cr_root_context,
                          "expected_results":1,
                          "content_to_be_requested":default_sub_process_amount}
        sub_f2_process={"prompt":Content_Result(prompt_followup2_rate,is_completed=True),
                          "context":cr_root_context,
                          "expected_results":1,
                          "content_to_be_requested":default_sub_process_amount}
        sub_f3_process={"prompt":Content_Result(prompt_followup3_rate,is_completed=True),
                          "context":cr_root_context,
                          "expected_results":1,
                          "content_to_be_requested":default_sub_process_amount}


        root_process=Process_Rewrite(body_of_task=cr_root_body,context=cr_root_context,prompt=cr_root_prompt,expected_results=1,
                                     content_to_be_requested=1,
                                     subprocess_tuple=(Process_Rate,sub_root_process)
                                     )
        followup_process=Process_Rewrite(body_of_task=cr_root_body,suggestion=root_process.get_final_results()[0],context=cr_root_context,prompt=cr_followup_prompt,
                                         expected_results=1,
                                         content_to_be_requested=4,
                                         subprocess_tuple=(Process_Rate,sub_f_process))

        followup_process2=Process_Rewrite(body_of_task=followup_process.get_final_results()[0],prompt=cr_followup_prompt2,
                                          expected_results=1,
                                          content_to_be_requested=4,
                                          subprocess_tuple=(Process_Rate,sub_f2_process)
                                          )
        followup_process3=Process_Rewrite(body_of_task=followup_process.get_final_results()[0],suggestion=followup_process2.get_final_results()[0],prompt=cr_followup_prompt3,
                                          expected_results=1,
                                          content_to_be_requested=4,
                                          subprocess_tuple=(Process_Rate, sub_f3_process)
                                          )




        #OTher TASK
        '''
         My 'adult' 23-year-old son is home for the holidays. He leads a more liberal lifestyle than my husband and me, and suffice it to say not only do our politics not match up, but neither do our hygiene practices. To be blunt, his body order is killing us! I didn't raise him this way and I absolutely can't stand it. I just can't embrace not showering daily and not using a daily dose of antiperspirant. How do you address an awkward and difficult topic with a person who is also awkward and difficult?

         List a couple (3-4 ideas) as to how handle answering this question in a way that is considerate and sensitive, but also deals with the problem. Provide an explanation as to how they would help.

        Using the suggestions and ideas on the left, write a response to the problem above attempting to be sensitive and sincere to the issue.

        Try to keep the style (but not the content), and incorporate the ideas and content described on the left to the best of your ability.
        '''



        #Tell your son, "We love having you home. But you've got to wash yourself --
        #  and your clothes -- while you're here. Let me show you how to use the washer, and let's put in a load."






        session.add(root_process)
        session.add(followup_process)
        session.add(followup_process2)
        session.add(followup_process3)


def setup_loop_again(session):
        root_sentence= "In Boston, there's a monument for the man who was the owner of one of the largest film production companies ever. In truth, " \
                       "he wasn't really the most amazing producer at all. He stole innocence and virtue from many women. While the man's monument still " \
                       "stands, how many people today know that these women were traumatized? Unfortunately, the monument is made from materials that last, " \
                       "and the lie has stood the test of time. This example shows you have to be vigilant with regards to the truth, especially when the lie " \
                       "itself is weak. These weak lies won't last more than the average truths"

        root_prompt="Rewrite this text to improve the general flow and feel of text as though it were a speech. Make sure that to incorporate the ideas on the bottom left." \
                    "Try to maintain the general structure, and sentence length"

        root_prompt_rate="Rate how well does the text below sound better than it's source material above. Also account for how well it incorporates the ideas and suggestions on the left"
        root_context="Men in power sexually assaulting women"

        body_of_task = Content_Result(root_sentence, is_completed=True)
        prompt = Content_Result(root_prompt, is_completed=True)
        context=Content_Result(root_context,is_completed=True)
        sub_process1_setting = {"prompt":Content_Result(root_prompt_rate,is_completed=True), "context":context,
                                "expected_results": 1,
                                "content_to_be_requested": 3
                                }

        root_process = Process_Rewrite(body_of_task=body_of_task, prompt=prompt, context=context,expected_results=1,
                                       content_to_be_requested=4,
                                       subprocess_tuple=(Process_Rate, sub_process1_setting))


        session.add(root_process)


def setup_meta(session):

    root_sentence= "There is in Boston a monument of the man who discovered anesthesia; many people are aware, in these latter days, " \
                   "that that man didn't discover it at all, but " \
                   "stole the discovery from another man. Is this truth mighty, " \
                   "and will it prevail? Ah no, my hearers, the monument is made of hardy material, but the lie " \
                   "it tells will outlast it a million years. An awkward, feeble, leaky lie is a thing which you ought to make it your unceasing study to avoid; such a lie as that " \
                   "has no more real permanence than an average truth."

    root_prompt = "Rewrite this as though it were written in contemporary english and modern times. You should try to keep the same number of sentences, as well " \
                  "as the general placement of nouns, adjectives and other parts of speech. "

    follow_up_prompt_suggestions = "What are some interesting contemporary issues and examples that you can think of where lying has impacted society, or you personally"


    root_prompt_rate = "How well does this text sound like it was written more like in modern times, as well as the overall quality"

    follow_up_prompt_suggestions_rate="Rate how well you feel the examples and issues provided are interesting?"


    end_prompt="Try to rewrite the text below to make it sound better as well as incorporate the suggestions and ideas discussed on the left. Attempt to maintain " \
               "the number of sentences, and general placement of nouns adjectives and other parts of speech.  " #do this twice
    end_prompt_rate="Rate how well the overall text sounds as well as how well it incorporated the suggestions and ideas on the left"

    default_rewrite_amount=1
    default_sub_process_amount=1


    body_of_task=Content_Result(root_sentence,is_completed=True)
    prompt=Content_Result(root_prompt,is_completed=True)

    sub_process1_setting={"prompt":Content_Result(root_prompt_rate,is_completed=True),
                          "expected_results":1,
                          "content_to_be_requested":default_sub_process_amount
                          }

    root_process=Process_Rewrite(body_of_task=body_of_task,prompt=prompt,expected_results=1,content_to_be_requested=1,
                                 subprocess_tuple=(Process_Rate,sub_process1_setting))
    session.add(root_process)

    #second task
    contemporary_issues_prompt=Content_Result(follow_up_prompt_suggestions,is_completed=True)
    sub_process2_setting = {"prompt": Content_Result(follow_up_prompt_suggestions_rate, is_completed=True),
                            "expected_results": 1,
                            "content_to_be_requested": default_sub_process_amount
                            }


    contemporary_issues=Process_Rewrite(prompt=contemporary_issues_prompt,expected_results=1,content_to_be_requested=1,
                                        subprocess_tuple=(Process_Rate,sub_process2_setting))


    final_output_prompt=Content_Result(end_prompt,is_completed=True)
    sub_process3_setting = {"prompt": Content_Result(end_prompt_rate, is_completed=True),
                            "expected_results": 1,
                            "content_to_be_requested": default_sub_process_amount,
                            "context":contemporary_issues.get_final_results()[0]
                            }

    final_outcome_1=Process_Rewrite(prompt=final_output_prompt,body_of_task=root_process.get_final_results()[0],
                                    context=contemporary_issues.get_final_results()[0],expected_results=1,content_to_be_requested=1,
                                    subprocess_tuple=(Process_Rate,sub_process3_setting)
                                    )

    sub_process4_setting = {"prompt": Content_Result(end_prompt_rate, is_completed=True),
                            "expected_results": 1,
                            "content_to_be_requested": default_sub_process_amount,
                            "context": contemporary_issues.get_final_results()[0]
                            }
    final_outcome_2 = Process_Rewrite(prompt=final_output_prompt, body_of_task=final_outcome_1.get_final_results()[0],
                                      context=contemporary_issues.get_final_results()[0], expected_results=1,
                                      content_to_be_requested=default_sub_process_amount,
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

    setup_summary(session )
    session.commit()
