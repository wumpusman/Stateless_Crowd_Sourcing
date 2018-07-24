from db_connection2 import *
from manager import Manager
import re
import os






sess=None


def produce_pairs (str_1,str_2):
    return [Content_Result(str_1, is_completed=True), Content_Result(str_2, is_completed=True)]

def build_process(Process_Type,prompts_ary,body,context,suggestions,amount_to_be_request_main,amount_to_be_requested_sub, expected_results=1):

    sub_process = {"prompt": prompts_ary[1],
                   "expected_results": 1,
                   "content_to_be_requested": amount_to_be_requested_sub}

    if context!=None: #technically unneccesary tbh
        sub_process["context"]=context
    if suggestions!=None:
        sub_process["suggestion"]=suggestions

    sub_process_type = Process_Rate
    process_type=Process_Type
    if(type(Process_Type)==type(())):
        process_type=Process_Type[0]
        sub_process_type=Process_Type[1]


    generated_process=process_type(body_of_task=body,prompt=prompts_ary[0],suggestion=suggestions,context=context,content_to_be_requested=amount_to_be_request_main,
                   expected_results=expected_results,
                   subprocess_tuple=(sub_process_type,sub_process)
                   )
    print generated_process
    generated_process.is_using_ml=True

    sess.add(generated_process)
    return generated_process


def build_process_flex(Process_Type,prompts_ary,body,context,suggestions,amount_to_be_request_main,amount_to_be_requested_sub, expected_results=1):

    return build_process((Process_Type,Process_Rate_Flex),prompts_ary,body,context,suggestions,amount_to_be_request_main,amount_to_be_requested_sub, expected_results=expected_results)



def evaluation_criteria(session,prompt,body,result, context,suggestion, min,max):



    prompt = Content_Result(prompt, True)
    result =Content_Result(result,True)
    context = Content_Result(context,True)
    suggestion = Content_Result(suggestion,True)
    body=Content_Result(body,True)
    pr = Process_Rate_Flex_Test_User(prompt=prompt, displayed_result=result, body_of_task=body, context=context,suggestion=suggestion,content_to_be_requested=1)
    pr.expected_result_min = min
    pr.expected_result_max = max
    session.add(pr)


def initial_test_criteria(session):
    prompt = "Rate how well the text in 'Content To Be Evaluated' answers the question: What is an analogous HUMAN behavior or a close equivalent to the behavior below and emotion, w. I.E. EXAMPLES Bird doing mating call -> ANSWER: A boy trying to pick up a girl."
    body = " The horses loved their mates and offspring."
    result = "The mother and father loved each other as much as they loved their children. "
    evaluation_criteria(session, prompt, body, result, None, None, 3, 10)


    prompt="Rate how well the text in 'Content To Be Evaluated' answers the question: Where would you see the behavior below listed in 'Original Content'. I.E. EXAMPLES A boy picking up a girl -> ANSWER At a bar"
    body=" A mother shielding their child from harm."
    result="A mother will put the safety of her children before herself"
    evaluation_criteria(session,prompt,body,result,None,None,-2,2)



def test_evaluation_criteria_example(session):
    global sess
    sess = session
    '''
                4. Where would you see this behavior. I.E. EXAMPLES A boy picking up a girl -> ANSWER At a bar
            
            A mother shielding their chid from harm.
            As a car mounted the pavement a mother frantically pulled her child out of its path. 
            
            Terrible answer: A mother will put the safety of her children before herself. 
            
            
            
            3. What is an analogous HUMAN behavior or a close equivalent to the behavior below and emotion, w. I.E. EXAMPLES Bird doing mating call -> ANSWER: A boy trying to pick up a girl.

The horses loved their mates and offspring.
The mother and father loved each other as much as they loved their children. 
    '''
    #A mother will put the safety of her children before herself.
    prompt = Content_Result("This is arbitrary, you should like it", True)
    result = Content_Result("I love you human", True)
    Process_Object()
    pr = Process_Rate_Flex_Test_User(prompt=prompt, displayed_result=result, content_to_be_requested=1)
    pr.expected_result_min = 4
    pr.expected_result_max = 5

    prompt = Content_Result("This is arbitrary, you should hate it", True)
    result = Content_Result("I hate life :(", True)
    Process_Object()
    pr2 = Process_Rate_Flex_Test_User(prompt=prompt, displayed_result=result, content_to_be_requested=1)
    pr2.expected_result_min = -2
    pr2.expected_result_max = 2

    test_write="Test fake content"
    test_rate="Rate fake content"
    test_process=build_process(Process_Rewrite,produce_pairs(test_write,test_rate),None,None,None,1,1,1)

    session.add(pr2)
    sess.add(pr)
    sess.add(test_process)


def test_flex(session):
    '''
    Basic idea to test variable changing levels of content

    :param session:
    :return:
    '''
    global sess
    sess=session
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]

    prompt,rate="tell me what the meaning of life is","rate how good this idea is"
    prompt1,rate1="Expand what this ideal means","rate how good this expansion is"
    context="Humanity is inferior to machines "

    build_process_flex(Process_Rewrite_Flex,produce_pairs(prompt,rate),body=None,suggestions=None,context=Content_Result(context,is_completed=True),
                       amount_to_be_request_main=2,amount_to_be_requested_sub=6)


def generate_shirt_design(session):
    global sess
    sess = session
    #Randomly pick an animal from the list you find interesting that has been well studied by humans. Piglets, Puppies, Penguins, Pigeons, Hedgehogs, Horses, Squirrels, Seals, Rats, Cats, Porcupines, Seals, Groundhogs, Lions, Zebras,
    # pick an emotion/relationship from the following that you could imagine the animal having towards another in its species: attraction/mating behavior, play, fear, happy, love, sadness, affection, seduction/mating behavior, child-parent affection
    #Given the emotion and the animal, google a social behavior that this animal does to express the emotion/behavior as well physical behavior associated with it. Write it below, and the motivation beyond it.
    #EX. DO not use these: kangaroos hop when fighting, hodeghods curl in fear,  brids regurgiate food to their young     dogs wag their tail and run when playing with other dogs, hedgehogs curl up when scared, Elephants touch each other snouts when distressed, horses will run with each other, hodeghods curl in fear, brids regurgiate food to their young

        #list name #list animal
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    default_process_amount, default_sub_process_amount = 2,5
    prompts = [
        "0. Randomly pick an animal from the list you find interesting. Piglets, Puppies, penguins, Hedgehogs, Horses, Elephants, Squirrels, Seals, Rats, Cats, Porcupines, Seals",
        "1. Pick an emotion/relationship from the following that you could imagine the animal having towards another in its species: attraction/mating behavior, play, fear, happy, love, sadness, affection, seduction/mating behavior, child-parent affection ",

        "2. Given the emotion and the animal expressed below and in 'Context' quickly google a social behavior that this animal does to express the emotion/behavior as well physical behavior associated with it. Write it below, and the motivation behind it.  \
        I.E. Kangaroos hop when fighting, hedgehogs curl in fear,  birds regurgiate food to their young ",

        "3. What is an analogous HUMAN behavior or a close equivalent to the behavior below and emotion, w.  I.E. EXAMPLES Bird doing mating call -> ANSWER: A boy trying to pick up a girl.",
        "4. Where would you see this behavior. I.E. EXAMPLES A boy picking up a girl -> ANSWER At a bar",
        "5. Describe the of kind of scenario/setting you imagine this to happen in. Context describes the location. I.E. EXAMPLES A boy picking up a girl -> He might be trying to grind on her on the dance floor",
        "6. Incorporate the information in main text to evaluate, context, and info into a single sentence. I.E. EXAMPLES A boy picking a girl AND he might be trying to grind on the dance floor -> A boy is grinding with a girl on \
         the dance floor in order to pick her up",
        "7. Given the animal listed in info, and the situation below, remove any mention of people, and replace or add the animal in  I.E. EXAMPLES Birds and 'A boy picking up a girl at a club \
         -> A male bird is trying to pick up a female bird at a club and grinding on the dance floor",
        "8. What other attributes of the following animal would you add to this description to make it feel more animal like. \
         I.E. Bird, Bird sings to attract females MAPPED to bird is picking up another bird at a club and trying to grind with her on a dance floor -> \
         The male birds wings are outstretched as it grinds on the dance floor. It's holding a beer glass full of worms",

        "9. How would you anthromorphize the animals and situation described in the scene to give them more humanlike qualities and make the situation more humanlike. I.E bird grinding on dance floor -> \
         Birds grinding on the dance floor are dressed in colorful suits and dresses. Both birds are holding drinks. Maybe other animals chilling at a bar. ",
        "10. Incorporate the information in a single description. I.E. bird grinding on dance floor AND birds could be holding drinks. -> Birds are grinding on the dance floor. \
         They are holding drinks. ",
        "11. Given the following surreal scene, and the animal behavior described in context, what are some questions, suggestions to flesh out the scene.  \
         I.E. Mating call of birds maps to Birds are grinding in a bar -> What kind of music, what is the disposition between the two animals, what kind of outfits are the birds wearing, what kind of bar is it (edm versus low key),\
         what's in the backdrop",
        "12. Given the surreal scene, and the questions listed below, try to answer them descriptively. I.E. Birds are dancing in a bar And What kind of outfits are they wearing -> The \
         . male is wearing a very colorful vest and female bird is wearing all black"

    ]

    how_many_versions = 3

    params=[{}]*len(prompts)
    params[0]={"process_amount":how_many_versions}
    params[2]={"name":"closest human behavior","context":0} #context is -2
    params[3]={"body":2,"context":0, "info":1} # "process_amount":2, "sub_amount":0
    params[5]={"body":4,"context":3}
    params[6]={"body":3, "context":5,"info":4}
    params[7]={"info":0,"context":2}
    params[8]={"body":7,"context":0,"info":2}
    params[9]={"body":7,"info":8,"context":0}
    params[10]={"context":7,"info":9}
    params[11]={"body":10,"context":2}
    params[12]={"body":11,"context":10, "info":1}
    #params[8]=
    rate = "Rate how well the text highlighted below achieves the following instruction: "

    rate_ary=[rate +"[ " +i+ " ]" for i in prompts]
    rate_ary[3]="Rate the highlighted content based on if it describes human behavior and how well it maps to the behavior described below." \
                " I.E. EXAMPLES Bird doing mating call -> ANSWER: A boy trying to pick up a girl."

    print rate_ary
    p_r_content_results=[]


    for i in xrange(len(prompts)):
        p_r_content_results.append(produce_pairs(prompts[i],rate_ary[i]))

    print "OK"
    get_process_result=lambda param_dict, element_name,process_list,which_version,which_result: None if param_dict.get(element_name)==None else process_list[param_dict.get(element_name)][which_version].get_final_results()[which_result]

    process_list=[]



    for i in xrange(0,len(prompts)):

        process_amount = default_process_amount if params[i].get("process_amount") == None else params[i].get(
            'process_amount')

        sub_process_amount = default_sub_process_amount if params[i].get("sub_amount") == None else params[i].get(
            'sub_amount')

        prompt_rate_pair=p_r_content_results[i]


        print prompt_rate_pair
        body= None
        info=None
        context=None

        process=None
        if i ==0: #
            process_list.append([])

            process = build_process_flex(Process_Rewrite_Flex, prompt_rate_pair, body, context, info, how_many_versions,
                                    sub_process_amount, how_many_versions)  # if it's the first one

            for i in xrange(how_many_versions):

                process_list[-1].append(process)


        else:

            process_list.append([])  # add extra section


            for j in xrange(how_many_versions):
                final_result_number=0 #which result to extract - shuold normally be 0 unless 0 is found

                if i-1==0:
                    final_result_number=j #if it is the 0th element then it should be the particular location



                body = process_list[i - 1][j].get_final_results()[final_result_number] if i > 0 else None  # default for body

                if params[i].get("body") != None:
                    relevant_number=0
                    if params[i].get("body")==0:
                        relevant_number=j

                    body = get_process_result(params[i], "body", process_list, j,relevant_number)
                if params[i].get("info") != None:
                    relevant_number = 0
                    if params[i].get("info")==0:
                        relevant_number=j
                    info = get_process_result(params[i], "info", process_list, j,relevant_number)

                if params[i].get("context") != None:
                    relevant_number = 0
                    if params[i].get("context")==0:
                        relevant_number=j
                    context = get_process_result(params[i], "context", process_list, j,relevant_number)





                process=build_process_flex(Process_Rewrite_Flex,prompt_rate_pair,body,context,info,process_amount,sub_process_amount,1)

                process_list[-1].append(process) #add each version of it


    return process_list





def iterative(session,general_about,main_text):
    global sess
    sess=session
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    default_process_amount = 3
    default_sub_process_amount = 3
    if general_about==None:
        general_about="Much like the Emancipation Proclamation one hundred years ago," \
                  " women are facing oppression in the workplace, even today. " \
                  "Women workers face discrimination in pay per worker salaries and hourly wages. "
    if main_text==None:
        main_text=" I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation. Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great beacon light of hope to millions of African American slaves who had been seared in the " \
                  "flames of withering injustice. It came as a joyous daybreak to end the long night of their captivity." \
                  " But one hundred years later, African Americans are still experiencing injustices." \
                  " For instance, many black women today are still experiencing sexism. "

    gen_about_cr=Content_Result(general_about,True)
    main_text_cr=Content_Result(main_text,True)


    prompt="Try to rewrite this to better emphasize and discuss sexism. Usethe roughly same number of sentences and general structure. " \
           "However, try to change the context and examples to be more appropriate to the topic of sexism. "
    rate="Rate how well this text better encapsulates the topic of sexism"
    pr=produce_pairs(prompt,rate)

    prompt1="Try to rewrite this to better emphasize and discuss sexism. Use roughly same number of sentences and general structure. " \
           "However, try to change the context and examples to be more appropriate to the topic of sexism. The text on left is meant to give you an idea " \
            "of what the rewritten should be about"
    rate1="Rate how well this text better encapsulates the topic of sexism"
    pr1=produce_pairs(prompt1,rate1)

    process=None
    for i in xrange(0,2):
        process=build_process(Process_Rewrite,pr,gen_about_cr,None,None,default_process_amount,default_sub_process_amount)
        gen_about_cr=process.get_final_results()[0]

    for i in xrange(0,4):
        process=build_process(Process_Rewrite,pr1,main_text_cr,gen_about_cr,None,default_process_amount,default_sub_process_amount)
        main_text_cr=process.get_final_results()[0]


def line_by_line_rewrite_with_flex_and_testing(session,steps1,str1):
    global sess
    sess = session
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    default_process_amount = 2
    default_sub_process_amount = 4

    if steps1 == None:
        steps1 = [" [Provide/Google/Search for historical context]", " [Elaborate the purpose behind the action]",
                  " [Clarify that action did not fully solve the underlying problem] "]
    if str1 == None:
        str1 = ["One hundred years ago the Emancipation Proclamation was signed by Abraham Lincoln",
                "This decree was insturmental in freeing the slaves and giving them hope " \
                "for a productive life free from chains. ", \
                "Yet, even today, the negro is not completly free from oppression"]
    str1_alt = []
    for i in xrange(len(str1)):
        str1_alt.append(". ".join(str1[0:i]) + " _EXAMPLE_RESULT_DIFFERENT_DOMAIN_ [" + str1[i:i + 1][0] + "]")

    stepsCr = [Content_Result(" _INSTRUCTIONS_ " + stp, True) for stp in steps1]
    exampleCr = [Content_Result(ex, True) for ex in str1_alt]

    if len(stepsCr) != len(exampleCr): raise Exception("AHH this can't be happening")

    prompt1 = "To best of your abilities write about the subject of the TREATMENT OF WOMEN using the instructions listed below in 'Main Text to Evaluate'. An example " \
              "in a different subject/domain is shown in INFO. THIS IS AN EXAMPLE for stylstic purposes. You may google if neccesary "
    rate1 = "Rate how well the content to be evaluated follows the instruction listed in Context to create a text appropriate to subject of the 'TREATMENT OF WOMEN' "
    pr1 = produce_pairs(prompt1, rate1)

    prompt2_with_work = "Listed below is text about the subject of the TREATMENT OF WOMEN, as well as instructions listed '[]'. Use those instructions to write the next " \
                        "sentence as it relates to the subject of the TREATMENT OF WOMEN. An example of a different domain/subject is shown in INFO "
    rate2 = "Rate how well the 'content to be evaluated' follows the instruction listed in Context to extend this piece of text in 'Original Content'"
    pr2 = produce_pairs(prompt2_with_work, rate2)

    rewrite1_full_process = build_process_flex(Process_Rewrite_Flex_Modify_Results_And_View, pr1, None, stepsCr[0], exampleCr[0]
                                          , default_process_amount, default_sub_process_amount)

    prev_step_result = rewrite1_full_process.get_final_results()[0]
    for i in xrange(1, len(exampleCr)):
        rewrite_rest_full_process = build_process_flex(Process_Rewrite_Flex_Modify_Results_And_View, pr2, prev_step_result
                                                  , stepsCr[i], exampleCr[i]
                                                  , default_process_amount, default_sub_process_amount)

        prev_step_result = rewrite_rest_full_process.get_final_results()[0]


def line_by_line_rewrite(session,steps1,str1):
    global sess
    sess=session
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    default_process_amount = 2
    default_sub_process_amount = 3

    if steps1==None:
        steps1=[" [Provide historical context]", " [Elaborate the purpose behind the action]", " [Clarify that action did not fully solve the underlying problem] "]
    if str1 ==None:
        str1=["One hundred years ago the Emancipation Proclamation was signed by Abraham Lincoln", "This decree was insturmental in freeing the slaves and giving them hope " \
         "for a productive life free from chains. ", \
         "Yet, even today, the negro is not completly free from oppression"]
    str1_alt=[]
    for i in xrange(len(str1)):
        str1_alt.append(". ".join(str1[0:i])+" _EXAMPLE_RESULT_DIFFERENT_DOMAIN_ ["+str1[i:i+1][0]+"]")

    stepsCr=[Content_Result(" _INSTRUCTIONS_ "+stp,True) for stp in steps1]
    exampleCr=[Content_Result(ex,True) for ex in str1_alt]

    if len(stepsCr)!=len(exampleCr): raise Exception("AHH this can't be happening")

    prompt1="To best of your abilities write about the subject of the treatment of women using the instructions listed below in 'Main Text to Evaluate'. An example " \
            "in a different subject/domain is shown in INFO "
    rate1 = "Rate how well the content to be evaluated follows the instruction listed in Context to create a text appropriate to subject of the 'treatment of women' "
    pr1=produce_pairs(prompt1,rate1)

    prompt2_with_work="Listed below is text about the subject of the treatment of women, as well as instructions listed '[]'. Use those instructions to write the next " \
                      "sentence. An example of a different domain/subject is shown in INFO "
    rate2 = "Rate how well the 'content to be evaluated' follows the instruction listed in Context to extend this piece of text in 'Original Content' It should NOT have any of" \
            "the information in INFO which is only meant as an example to aid in writing the style or format."
    pr2=produce_pairs(prompt2_with_work,rate2)



    rewrite1_full_process = build_process(Process_Modify_Results_And_View, pr1, None,stepsCr[0],exampleCr[0]
                                           , default_process_amount, default_sub_process_amount)


    prev_step_result = rewrite1_full_process.get_final_results()[0]
    for i in xrange(1,len(exampleCr)):

        rewrite_rest_full_process = build_process(Process_Modify_Results_And_View, pr2,prev_step_result
                                          , stepsCr[i], exampleCr[i]
                                          ,default_process_amount, default_sub_process_amount)

        prev_step_result=rewrite_rest_full_process.get_final_results()[0]




def speech_rewrite_linear(session):
    sess=session
    #to the best of your ability in a few sentences summarize what is being said. The information on the right (if available) describes the context
    #The information on the left describes an ongoing piece of writting. The text below is a continuation of it. To the best of your ability summarize, the text below.
    #Take the root of the speech
    #what are some issues that are relevant to you
    #Rewrite this speech to best account for these issues

    #The information on the left describes a summary piece of writing. The below is meant to be a piece from that original writing,
    # Modify the text below under "REWRITE BELOW" to better match the ideas and message of the summary on the left
    #
    pass


def rewrite_through_analogy(session,sum_text,full_text):
    global sess
    sess=session

    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    default_process_amount = 3
    default_sub_process_amount = 3

    body_of_sum=sum_text
    if full_text=="":
        full_text="I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation.  " \
                  "  Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. " \
                  "This momentous decree came as a great beacon light of hope to millions of Negro slaves who had been seared in the flames of withering injustice." \
                  " It came as a joyous daybreak to end the long night of their captivity.    But one hundred years later, the Negro still is not free"
    if body_of_sum == "":
        body_of_sum="One hundred years ago the Emancipation Proclamation was signed by Abraham Lincoln. This decree was insturmental" \
                " in freeing the slaves and giving them hope for a productive life free from chains. " \
                "Yet, even today, the negro is not completly free from oppression"




    body_of_sum_cr=Content_Result(body_of_sum,True)
    body_of_full_text_cr=Content_Result(full_text,True)


    rewrite_sum_prompt="The text below describes part of speech about racism. Try to rewrite this to incorporate and discuss sexism. Use" \
                       "the roughly same number of sentences and general structure. However, try to change the context and examples to be " \
                       "more appropriate to the topic of sexism."

    rewrite_sum_rate ="Rate how well the text on the right feels it incorporates the theme of sexism but keeps the structure and style of the text below"
    rewrite_sum_pr1=produce_pairs(rewrite_sum_prompt,rewrite_sum_rate)



    #TWO VARIATIONS

    rewrite_analogous_text_prompt="The text below is an expansion of the summary written in Info on the left. Try to rewrite the "\
                                "  text below to instead better match the ideas and context of the summary written in Context on the left. Try to use the general structure (i.e." \
                                  " sentence number, length, structure) " \
                                  " of the text below, but try to incorporate and match the themes and content of the text in Context. "

    rewrite_analogous_text_rate="Rate how well the text on the right feels like it incorporates the themes of the text in Context but keeps the structure and style " \
                                "of the text below (word structure, flow, quality of writing) "
    rewrite_anag_pr=produce_pairs(rewrite_analogous_text_prompt,rewrite_analogous_text_rate)




    rewrite_analogous_text_prompt_alt="The text on the left in Context consists of an elaboration/expansion of a summary written in Info. In the same way" \
                                        " try to expand/elaborate on the text written below. To inform the general structure (i.e. number sentence, length, structure, general grammar) use" \
                                      " the text in Context but match the themes and content written below"

    rewrite_analogous_rate_prompt_alt="Rate how well the text to be rated expands on the ideas and themes written below, AND keeps the structure and style of the text " \
                                      " listed in Context . "

    rewrite_alt_pr=produce_pairs(rewrite_analogous_text_prompt_alt,rewrite_analogous_rate_prompt_alt)

    rewrite_sum1_process = build_process(Process_Rewrite, rewrite_sum_pr1, body_of_sum_cr, None, None,
                                      default_process_amount, default_sub_process_amount)


    rewrite_anag_process=build_process(Process_Rewrite, rewrite_anag_pr,body_of_full_text_cr, rewrite_sum1_process.get_final_results()[0],
                                        body_of_sum_cr, default_process_amount, default_sub_process_amount)


    rewrite_anag_process_alt=build_process(Process_Rewrite,rewrite_alt_pr,rewrite_sum1_process.get_final_results()[0],body_of_full_text_cr,body_of_sum_cr,
                                           7, 1
                                           )



    Ver21_rewrite_analogous_idea_prompt="If someone were trying to create an analogous/similar text about sexism, what are  suggestions you would propose for new appropriate  " \
                                       "examples and references that would better match the theme of sexism (try to make suggestions for each sentence). I.E. relevant events, analogies, ideas, wording that relate to topic" \
                                        "of sexism instead of racism"

    Ver21_rewrite_analogous_idea_rate="Rate how well you feel the ideas would be useful in rewriting the text to be about a different subject such as sexism"
    rewrite21_idea_pr1 = produce_pairs(Ver21_rewrite_analogous_idea_prompt, Ver21_rewrite_analogous_idea_rate)

    Ver22_convert_prompt="The text below describes part of speech about racism. Try to rewrite this to incorporate and discuss sexism. Use" \
                       " the roughly same number of sentences and general structure. However, try to change the context and examples to be " \
                       " more appropriate to the topic of sexism. You may use the ideas listed in INFO to help edit and rewrite the text"

    Ver22_convert_rate=rewrite_sum_rate
    rewrite22_convert_pr1 = produce_pairs(Ver22_convert_prompt, Ver22_convert_rate)


    Ver23_convert_full_body_idea_prompt="Looking at the text below, if someone were trying to create an analogous/similar text that better matched the themes and content of " \
                                        " the summary listed in Context, what are suggestions you would propose for new appropriate examples and references (try to make suggestions for each " \
                                        " sentence). I.e. making more topical references" \
                                        " examples, references and wording so that the text was more themetically linked to the summary in Context "

    Ver23_convert_full_body_idea_rate="Rate how well you feel the ideas would be useful in rewriting the text below to fit the topics and themes listed in Context"
    rewrite23_convert_pr1 = produce_pairs(Ver23_convert_full_body_idea_prompt, Ver23_convert_full_body_idea_rate)



    Ver24_convert_full_body_incorporate_prompt="Try to rewrite the text below to incorporate and match the themes and content of the summary written in Context. I.e. Keep the general structure (i.e." \
                                  " sentence number, length, structure) " \
                                  " of the text below, but try to incorporate and match the themes and content of the text in Context. You may use the ideas listed in INFO" \
                                               " to help edit and rewrite the text below "
    Ver24_convert_full_body_incorporate_rate = "Rate how well the text on the right feels like it incorporates the themes of the text on the left but keeps the structure and style " \
                                " of the text below (word structure, flow, quality of writing) "

    rewrite24_convert_pr1 = produce_pairs(Ver24_convert_full_body_incorporate_prompt, Ver24_convert_full_body_incorporate_rate)

    #Processses
    ver21_process_idea=build_process(Process_Rewrite,rewrite21_idea_pr1,body_of_sum_cr,None,None,
                                           default_process_amount, default_sub_process_amount
                                           )

    rewrite22_convert_process=build_process(Process_Rewrite,rewrite22_convert_pr1,body_of_sum_cr,None,ver21_process_idea.get_final_results()[0], default_process_amount, default_sub_process_amount
                                           )

    rewrite23_full_idea_process = build_process(Process_Rewrite, rewrite23_convert_pr1, body_of_full_text_cr, rewrite22_convert_process.get_final_results()[0],
                                          None, default_process_amount,
                                          default_sub_process_amount
                                          )
    rewrite24_full_process = build_process(Process_Rewrite, rewrite24_convert_pr1, body_of_full_text_cr,
                                                rewrite22_convert_process.get_final_results()[0],
                                           rewrite23_full_idea_process.get_final_results()[0], 7,
                                                1
                                                )



    #alt Deconstruct

    Ver31_rewrite_analogous_idea_prompt = "The text below describes a synoposis of a speech. For each sentence, describe at a high level what " \
                                          "each sentence is doing/serving. For instance, these are examples of higher level 'making a claim to grab listener', 'giving an example to emphasize a point', 'reiteration of a previous statement" \
                                          " with more emotion'," \
                                          " 'follow up on what was said earlier', 'elaboration of idea to clarify claim', 'personal self disclosure to connect to listener','seguing to new idea' "

    Ver31_rewrite_analogous_idea_rate = "Rate how well you feel the high level descriptions capture what is happening on each line of text. "
    rewrite31_idea_pr1 = produce_pairs(Ver31_rewrite_analogous_idea_prompt, Ver31_rewrite_analogous_idea_rate)

    Ver32_convert_prompt = "The text below describes part of speech about racism. Try to rewrite this to incorporate and discuss sexism. Use" \
                           " the roughly same number of sentences and general structure. However, try to change the context and examples to be " \
                           " more appropriate to the topic of sexism. You may use the structure listed in INFO to help frame what is written "

    Ver32_convert_rate = rewrite_sum_rate
    rewrite32_convert_pr1 = produce_pairs(Ver32_convert_prompt, Ver32_convert_rate)

    Ver33_convert_full_body_idea_prompt = "Looking at the text below, for each sentence, describe at a high level what each sentence is doing/serves. " \
                                          " For instance, these are examples of higher level 'making a claim to grab listener', 'giving an example to emphasize a point', 'reiteration of a previous statement" \
                                          " with more emotion'," \
                                          " 'follow up on what was said earlier', 'elaboration of idea to clarify claim', 'personal self disclosure to connect to listener','seguing to new idea' "


    Ver33_convert_full_body_idea_rate = "Rate how well you feel the text captures at a high level what each sentence is conceptually describing"
    rewrite33_convert_pr1 = produce_pairs(Ver33_convert_full_body_idea_prompt, Ver33_convert_full_body_idea_rate)

    Ver34_convert_full_body_incorporate_prompt = "Try to rewrite the text below to incorporate and match the themes and content of the summary written in Context. I.e. Keep the general structure (i.e." \
                                                 " sentence number, length, structure) " \
                                                 " of the text below, but try to incorporate and match the themes and content of the text in Context. You may use the high level structure listed in INFO" \
                                                 " to help frame how you are going to rewrite the text below "
    Ver34_convert_full_body_incorporate_rate = "Rate how well the text on the right feels like it incorporates the themes of the text in Context but keeps the structure and style " \
                                               " of the text below (word structure, flow, quality of writing) "

    rewrite34_convert_pr1 = produce_pairs(Ver34_convert_full_body_incorporate_prompt,
                                          Ver34_convert_full_body_incorporate_rate)

    # Processses
    ver31_process_idea = build_process(Process_Rewrite, rewrite31_idea_pr1, body_of_sum_cr, None, None,
                                       default_process_amount, default_sub_process_amount
                                       )

    rewrite32_convert_process = build_process(Process_Rewrite, rewrite32_convert_pr1, body_of_sum_cr, None,
                                              ver31_process_idea.get_final_results()[0], default_process_amount,
                                              default_sub_process_amount
                                              )

    rewrite33_full_idea_process = build_process(Process_Rewrite, rewrite33_convert_pr1, body_of_full_text_cr,
                                                None,
                                                None, default_process_amount,
                                                default_sub_process_amount
                                                )
    rewrite34_full_process = build_process(Process_Rewrite, rewrite34_convert_pr1, body_of_full_text_cr,
                                           rewrite32_convert_process.get_final_results()[0],
                                           rewrite33_full_idea_process.get_final_results()[0], 7,
                                           1
                                           )


def stories_of_power_dynamics(session):
    global sess
    sess=session
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    default_process_amount=3
    default_sub_process_amount=3

    situation_prompt="In several sentences (more detail is preferable) describe a personal experience or of someone you know where a women in power abused her authority over " \
                     "another women (i.e. humilates, harrasses, hurts, etc). If you cannot think of one you can also describe a story you have heard about "
    situation_rate="Rate how well you feel the text below describes an realistic but significant life experience where a women in power abused her authority over " \
                     "another women (i.e. humilates, harrasses, hurts, etc) "
    sit_pr = produce_pairs(situation_prompt, situation_rate)

    follow_up_prompt="For the situation described what are some questions that you would ask the author to be better flesh out the scene and the relationship of the characters."
    follow_up_rate="Rate how well the questions below would help flesh out the scene and make a more grounded realistic scene"
    follow_pr = produce_pairs(follow_up_prompt, follow_up_rate)

    suggestion_prompt="Using the situation described as background (about abuse of power of authority between two women), try to answer the questions below. Try to find answers that would make more for a more realistic scene  "
    suggestion_rate="Rate how well the answers belows answer the question to help make the scene on the left sound more realistic"
    suggestion_pr=produce_pairs(suggestion_prompt,suggestion_rate)

    reconciliation_prompt="Reading the scene and background information on the left, propose a few realistic ways (be it an event, experience, discussion) the two could reconcile and find common ground with one another"
    reconciliation_suggestion="Reading the scene and background information on the left, rate how well the ideas would realistically help the characters reconcile "
    reconcile_pr=produce_pairs(reconciliation_prompt,reconciliation_suggestion)

    situation_process = build_process(Process_Rewrite, sit_pr, None, None, None, 8,
                                 default_sub_process_amount,3)

    for i in xrange(0,3):
        print "here is I"
        print i
        follow_up_process = build_process(Process_Rewrite,follow_pr,situation_process.get_final_results()[i],None,None,default_process_amount,default_sub_process_amount)


        suggestion_process=build_process(Process_Rewrite,suggestion_pr,follow_up_process.get_final_results()[0],situation_process.get_final_results()[i],None,
                                          default_process_amount,default_sub_process_amount)

        reconcile_process=build_process(Process_Rewrite,reconcile_pr,None,suggestion_process.get_final_results()[0],situation_process.get_final_results()[i],
                                          default_process_amount,default_sub_process_amount)


def travel_plan(session):
    #You're trying to design an interesting and unique vacation plan to visit NYC.
    #To achieve this goal, what's the first thing you would do to reseach/plan this trip. Given an example of what you would do first to plan, and explain why.
    #You're planning to go to nyc, and you're currently doing the following: '' To achieve this goal, what would you need to do,  why, give example
    #make this a descending treee
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    default_sub_process_amount = 2
    default_process_amount = 3

    nyc_trip_prompt = "You're trying to think up an interesting and unique vacation plan to visit NYC. In a few sentences, what's the most immediate thing you would you" \
               "do to plan/reserach for it"
    nyc_trip_rate = "Rate how well you feel the idea listed would be helpful in planning/researching an interesting and unique vacation."


    One_pr = produce_pairs(date_plan_prompt1, date_plan_rate1)
    pass


def date_plan(session):
    global sess
    sess=session
    # Friend is trying to figure out what to do on a date, what are some questions you would ask him to help flesh out what he should do
    # ANSWEr them kEENAN
    # Given the answers, what is the first thing this person should do on a date
    # Given the following activity for a date, and the answers listed, what are some questions to help them flesh out what would make this date/activity interesting
    # Answer them keenan
    # Given the answers, flesh out what he should do for this activity
    produce_pairs=lambda a,b: [Content_Result(a, is_completed=True),Content_Result(b,is_completed=True)]
    default_sub_process_amount = 2
    default_process_amount = 3

    date_plan_prompt1="A friend is trying to figure out what to do next on a date, what are some questions you would ask him to help flesh out what he should do. Any information on the " \
                      "left or below is meant to provide context about their date so far and background information"
    date_plan_rate1="Rate how well you feel the content would help a person flesh out what to do on a date."
    One_pr=produce_pairs(date_plan_prompt1,date_plan_rate1)

    #KEENAN TASK
    answer_prompt2="Using full sentences, answer the following questions to the best of your ability in those circumstances. The answers are helping to inform a date decision"
    answer_rate2="Rate how well you feel the content answers the questions listed below"
    Two_answer_p_r2=produce_pairs(answer_prompt2,answer_rate2)

    suggestion_prompt3="A friend is trying to figure out an ideal date. THe information on the left describes additional information about the person and their previous plans. To the best of your ability " \
                        "what should they do next on the date"
    suggestion_rate3="Rate how well you feel the suggestion would make for a good date"
    Three_sugg_pr3=produce_pairs(suggestion_prompt3,suggestion_rate3)


    date_sub_plan_prompt="A friend is trying to figure out what would engage a date during one of the activities listed below. What are some questions you would ask him to help flesh out" \
                  "what they should do during that activity to make it more fun."
    date_sub_plan_rate="Rate how well you feel the questions below would help a person flesh out what to do during the date activity below."
    date_sub_plan_p_r=produce_pairs(date_sub_plan_prompt,date_sub_plan_rate)


    answer_sub_prompt="Using full sentences, answer the following questions to the best of your ability. The answers are helping to inform the structure of a date activity"
    answer_sub_rate="Rate how well you feel the answer's address address the questions listed below"
    answer_sub_p_r=produce_pairs(answer_sub_prompt,answer_sub_rate)

    incorporate_sub_prompt="Using the description of the date activity, and the answers below, describe what you would do during the date activity to make it fun"
    incorporate_sub_rate="Rate how well you feel the content below fleshes out what you would during the date activity"
    incorporate_sub_p_r=produce_pairs(incorporate_sub_prompt,incorporate_sub_rate)

    summary_so_far_prompt="Reading the information below, and the information on the left, more concisely describe what the date plan is so far"
    summary_so_far_rate="Rate how well the content below describes the current date plan"
    summary_so_far_pr=produce_pairs(summary_so_far_prompt,summary_so_far_rate)


    body_current=Content_Result("",is_completed=True)



    #######################################
    for i in xrange(2):
        date_process = build_process(Process_Rewrite, One_pr, None , body_current, None, default_process_amount,
                                     default_sub_process_amount)

        answer_process =build_process(Process_Rewrite,Two_answer_p_r2,date_process.get_final_results()[0],
                                      body_current,
                                      None,default_process_amount,default_sub_process_amount)


        suggestion_process = build_process(Process_Rewrite, Three_sugg_pr3, body_current, None,
                                        answer_process.get_final_results()[0],
                                        default_process_amount,default_sub_process_amount
                                           )


        sub_date_process=build_process(Process_Rewrite,date_sub_plan_p_r,suggestion_process.get_final_results()[0],None,
                               None, default_process_amount,default_sub_process_amount
                               )


        sub_answer_process=build_process(Process_Rewrite,answer_sub_p_r,sub_date_process.get_final_results()[0],suggestion_process.get_final_results()[0],None,
                                         default_process_amount,default_sub_process_amount)


        sub_incorporate_process=build_process(Process_Rewrite,incorporate_sub_p_r,sub_answer_process.get_final_results()[0],suggestion_process.get_final_results()[0],None,
                                              default_process_amount,default_sub_process_amount)


        summary_process=build_process(Process_Merge,summary_so_far_pr, body_current,suggestion_process.get_final_results()[0],answer_process.get_final_results()[0],
                                      default_process_amount,default_sub_process_amount
                                      )

        body_current=summary_process.get_final_results()[0]


    session.commit()


def math_plan(session):
    pass
    # Trying to solve a critical thinking problem abotu the following. To help solve this problem, what is the first thing you would do
    # Goal + Y what is the next thing you would do


def question_answer_profile_generation(session, assign_user=True,text_body=""):
    global sess
    sess = session
    keenan =None

    keenan_list=session.query(User).filter(User.name == "Keenan").all()
    if len(keenan_list) ==0:
        keenan=User("Keenan")
        password="123abc"
        keenan.password=password
    else:
        keenan=keenan_list[0]



    produce_pairs=lambda a,b: [Content_Result(a, is_completed=True),Content_Result(b,is_completed=True)]
    default_sub_process_amount = 3
    default_process_amount = 3


    body=text_body
    One_body=Content_Result(body,is_completed=True)

    date_prompt1="A person is trying to create an about me for a dating profile. Given their profile what are some questions or suggestion you would ask them to help flesh out and improve their profile"
    date_rate1="Rate how well you feel the content and questions would help a user think about and improve the dating profile listed below."


    One_date_p_r1=produce_pairs(date_prompt1,date_rate1)

    #KEENAN TASK
    answer_prompt2="Pretend the profile on the left was your own, given your own personal knowledge, answer the following questions to the best of your ability."
    answer_rate2="Rate how well you feel the content on the right answers the questions listed below"
    Two_answer_p_r2=produce_pairs(answer_prompt2,answer_rate2)



    incorporate_prompt3="The text below is an about me for a dating profile. THe information on the left describes additional information about the person. To the best of your ability " \
                        "try " \
                        "to incorporate that information into the profile below"
    incorporate_rate3="Rate how well the content synthesizes the information on the left with the profile description listed below"

    Three_incorp_p_r_3=produce_pairs(incorporate_prompt3,incorporate_rate3)




    suggestion_prompt4="The text below is a part of a dating profile, provide specific suggestions of what you would remove, add or change to make this profile more engaging"
    suggestion_rate4="Rate how well you feel the content would help to improve the text listed below"
    Four_suggest_p_r4=produce_pairs(suggestion_prompt4,suggestion_rate4)

    #KEENAN TASK
    incorporate_prompt5="The text below is an about me of a dating profile, using the suggestions on the left, try to rewrite the profile to be more engaging"
    incorporate_rate5="Rate how well you feel the content improves the dating profile listed below"

    Five_incorporate_p_r4=produce_pairs(incorporate_prompt5,incorporate_rate5)


    for i in xrange(3):
        date_process = build_process(Process_Rewrite, One_date_p_r1, One_body, None, None, default_process_amount,
                                     default_sub_process_amount)

        answer_process= None
        if assign_user == False:
            answer_process = build_process(Process_Rewrite, Two_answer_p_r2, date_process.get_final_results()[0], One_body,
                                           None, default_process_amount, default_sub_process_amount)
        else:

            answer_process = build_process(Process_Rewrite, Two_answer_p_r2, date_process.get_final_results()[0],
                                           One_body,
                                           None, 1, 1)
            answer_process.assign_user(keenan)


        incorporate_process1=build_process(Process_Rewrite,Three_incorp_p_r_3,One_body,answer_process.get_final_results()[0],
                                           None,default_process_amount,default_sub_process_amount)

        suggestion_process=build_process(Process_Rewrite,Four_suggest_p_r4,incorporate_process1.get_final_results()[0],None,None,default_process_amount,default_sub_process_amount)

        incorporate_process2=build_process(Process_Rewrite,Five_incorporate_p_r4,incorporate_process1.get_final_results()[0],
                                           None,suggestion_process.get_final_results()[0],default_process_amount,default_sub_process_amount)

        One_body=incorporate_process2.get_final_results()[0]


    session.commit()

    '''
    sub_process = {"prompt": cr_prompt_rate,
                   "expected_results": 1,
                   "context":right_content_result,
                   "content_to_be_requested": default_sub_process_amount}

    merge_process = Process_Merge(body_of_task=left_content_result, context=right_content_result, prompt=cr_prompt,
                                      expected_results=1, content_to_be_requested=default_process_amount,
                                    subprocess_tuple=(Process_Rate,sub_process))

    merge_process.is_using_ml=True

    session.add(merge_process)
    session.commit()
    return merge_process
    '''
    #A person is trying to create an about me for a dating profile
    #listed below is the current state of it
    #Given their profile What are some questions or suggestion you would ask them to help flesh out and improve their profile


    #Given the profile on the right and your own personal knowledge, Answer the following questions to the best of your ability. Make sure your
    #answer is clarifying the question. I.E. what is your favorite activity? -> My favorite activity is running

    #The text below is an about me for a dating profile. THe information on the right describes additional information about the person. To the best of your ability try
    #to incorporate that information into the profile below

    #The text below is an about me of a profile, provide specific suggestions of what you would remove, add or change to make this profile more engaging

    #Using the suggestions on the left, try modify the text below to create a more interesting about me for a dating profile

def ideal_partner_generation(session):
    pass
    #THe person is trying to figure out what kind of person they want to date, the profile below lists what they are intersted in
    #Given the information, what are some questions you ask them to better flesh out the kind person/relationship they would want

    #Rate how well you feel the questions and suggestions below would help the person flesh out the kind of person/relationship they would want

    #Answer these questions KEENAN, DESTROYER OF WORLDS

    #Given the description and the answers on the left, try to rewrite the description of the kind of person they want to date

    #Step 1 + Answers


def rewrite_continuously(session,text_name):
    global sess
    sess=session
    default_process_amount=2
    default_sub_process_amount=5
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    root_body="The young girl sat wearily under the beautiful Christmas tree and tried vainly to ignore the cold and wet. One foot was damp because one " \
              "slipper had been stolen by her irritating brother, and having run from her house to escape from her violent Father, she had not had time to " \
              "put her boots on.  Trying to take comfort from the memories of her loving Grandmother and the stories she told of stars she lit the last of" \
              " her matches in a futile effort to stay warm.  Before the match goes out she sees the beauty of the tree and stars, a vision of her beloved " \
              "Grandmother appears welcoming her soul to heaven as her body freezes and dies."
    cr_root_body=Content_Result(root_body,is_completed=True)
    #root_prompt1 = "Rewrite this as though it were written in contemporary english and modern times. You should try to keep the same number of sentences, as well " \
     #             "as the general placement of nouns, adjectives and other parts of speech. "
    #KEENAN TASK
    root_prompt1="What ideas, details and concepts would make this story feel more like this was taking place in modern times. Briefly explain why."
    root_rate1="Rate how well you feel the ideas and concepts suggested would make the story below feel more modern and engaging."
    root_p_r1=produce_pairs(root_prompt1,root_rate1)
    root_process1=build_process_flex(Process_Rewrite_Flex_Modify_View, root_p_r1, cr_root_body,None , None, default_process_amount,
                  default_sub_process_amount)

    rewrite_prompt2="Rewrite the text below using the ideas and concepts suggested on the left. You should try to keep the same number of sentences as well as " \
                    "well as the general placement of nouns, adjcetives and other parts of speech."
    rewrite_rate2="Rate how well you feel the rewrite of the text captures the ideas and concepts suggested in context. "
    rewrite_p_r2=produce_pairs(rewrite_prompt2,rewrite_rate2)
    rewrite_process2=build_process_flex(Process_Rewrite_Flex_Modify_View, rewrite_p_r2, cr_root_body, None,root_process1.get_final_results()[0], default_process_amount,
                  default_sub_process_amount)

    relevant_text=break_up_text(text_name,5)

    rewrite_segment_prompt_N="Rewrite the text listed in  'CURRENT PART' to make it feel more modern, the themes and vibe described in INFO are meant to provide" \
                             "context for what the entire story is about. " \
            "You should try to keep the same number of sentences as well as well as the general placement of nouns, adjectives and other parts of speech in " \
                             "'CURRENT PART'. " \
                    "The text in 'Preceeding Text' describes what happened right before "
    rewrite_segment_rate_N="Rate how well you feel the text feels like it is a more contemporary story. The text should still have a similar flow to the " \
                           "version listed below" \
                     ""
    rewrite_p_rN=produce_pairs(rewrite_segment_prompt_N,rewrite_segment_rate_N)

    previous_time_step=Content_Result("",True)
    for text_block in relevant_text:
        relevant_block=Content_Result(text_block,True)
        rewrite_segments_process=build_process_flex(Process_Rewrite_Flex_Modify_View,rewrite_p_rN,relevant_block,previous_time_step,rewrite_process2.get_final_results()[0],
                                           default_process_amount,default_sub_process_amount
         )

        previous_time_step=rewrite_segments_process.get_final_results()[0]

    session.commit()
    #The text above second part describes the preceding narrative/text."




    #What ideas, details concepts would make this story feel more like this was taking place in modern days.4

    #Rewrite the text below using the ideas and concepts suggested on the left. You should try to keep the same number of sentences as well as
    #well as the general placement of nouns, adjcetives and other parts of speech.

    #Root_Prompt.

    #Rewrite the text listed below "Second Part" to better fit the ideas and concepts listed in info. You should try to keep the same number of sentences ....
    #The text above second part describes the preceding narrative/text.


def break_up_text(file_name, batch_size=5):
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    dir_path = os.path.join(dir_path, "backend/" + str(file_name))
    file = None
    file_text = None
    try:
        file = open(file_name, "rb")
    except:
        file = open(dir_path, "rb")
    file_text = file.read()
    file_text = file_text.replace("\n", "")
    file.close()
    file = file_text

    as_arry = re.split("[.;?]", file)
    # as_arry=as_arry[0:len(as_arry)/2]
    file_batch_size_5 = []
    for i in xrange(0, len(as_arry), batch_size):
        batch = ".".join(as_arry[i:i + batch_size])
        # batch=re.sub(r"[^u0000-u007F]+"," ",batch)
        file_batch_size_5.append(batch)

    return file_batch_size_5
    # print malcom_batch_size_5[1]

def setup_general_summary(session,file_name):
    file_batch_size_5=break_up_text(file_name)
    recurse_summary(session, file_batch_size_5, 0, None, file_batch_size_5)


def setup_luther(session):
    setup_general_summary(session,"luther_speech")

def setup_malcom_summary(session):
    setup_general_summary(session,"malcom_speech")
    '''
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    dir_path = os.path.join(dir_path, "backend/malcom_speech")
    malcom_speech = None
    try:
        malcom_speech = open("malcom_speech", "rb")
    except:
        malcom_speech = open(dir_path, "rb")
    malcom_speech_text = malcom_speech.read()
    malcom_speech_text=malcom_speech_text.replace("\n","")
    malcom_speech.close()
    malcom_speech = malcom_speech_text

    as_arry = re.split("[.;?]", malcom_speech)
    # as_arry=as_arry[0:len(as_arry)/2]
    malcom_batch_size_5 = []
    for i in xrange(0, len(as_arry), 5):
        malcom_batch_size_5.append(".".join(as_arry[i:i + 5]))
    print len(malcom_batch_size_5)
    #print malcom_batch_size_5[1]
    recurse_summary(session, malcom_batch_size_5, 0, None, malcom_batch_size_5)
    '''

def setup_remapped_linear_abstract(session,text_name):
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    global sess
    sess = session
    blocks=break_up_text(text_name)

    prompt1="At a highlevel write out what each sentence is trying to say"
    prompt2="In simple conceptual blocks write what is happening using the highlevel and original text as examples"
    prompt3="Rewrite the text to better map to your new one"

    p1,p2,p3=produce_pairs(prompt1,""),produce_pairs(prompt2,""),produce_pairs(prompt3,"")
    pr_list=[]
    index=0
    prev_raw=None
    prev_gen=None
    prev_new=None

    past_text=None
    for i in blocks:
        if index>0:
            prev_raw=pr_list[index-1][0].get_final_results()[0]
            prev_gen=pr_list[index-1][1].get_final_results()[0]
            prev_new=pr_list[index-1][2].get_final_results()[0]
            past_text=pr_list[index-1][3]

        current_text=Content_Result(i,is_completed=True)
        raw=build_process(Process_Rewrite,p1,current_text,
                    past_text,prev_new,amount_to_be_request_main=1,amount_to_be_requested_sub=0)
        gen_idea=build_process(Process_Rewrite,p2,raw.get_final_results()[0],context=current_text,
                               suggestions=prev_gen, amount_to_be_request_main=1, amount_to_be_requested_sub=0)

        new_version=build_process(Process_Rewrite,p3,gen_idea.get_final_results()[0],context=current_text,
                               suggestions=prev_new, amount_to_be_request_main=1, amount_to_be_requested_sub=0)

        index+=1
        pr_list.append((raw,gen_idea,new_version,current_text))


def setup_sedaris_high_level(session):
    #setup_general_summary(session,'sedaris')
    #to_basic_element_process= session.query(Process_Rewrite).all()
    root=session.query(Process_Text_Manipulation).filter(Process_Text_Manipulation.id == 127).all()[0]
    produce_pairs = lambda a, b: [Content_Result(a, is_completed=True), Content_Result(b, is_completed=True)]
    global sess
    sess = session


    prompt_for_conceptual_idea="Text below describes a synoposis of text, at a high level what is it trying to say"
    rate_conceptual_idea="Rate how  well this describes the general ideas of the text"
    abstract_pair=produce_pairs(prompt_for_conceptual_idea,rate_conceptual_idea)

    prompt_for_rewrite="write the text to better match the ideas expressed on the left. The text on left is an example, and text above it provides some context "
    rate_rewrite="rate how good rewrite feels"
    remap_pair=produce_pairs(prompt_for_rewrite,rate_rewrite)



    def recurse_down(session,parent_process, el, first_pair,second_pair):
        global sess
        sess = session



        if el == None:
            return


        parent_result=None
        if parent_process!=None:
            parent_result=parent_process.get_final_results()[0]


        #first method
        abstracted_process=build_process(Process_Rewrite, first_pair, el.get_final_results()[0],parent_result, None,
                      1, 1)

        # first method
        rewrite_process=build_process(Process_Rewrite, second_pair, abstracted_process.get_final_results()[0], parent_result
                                      , el.get_final_results()[0],
                      1, 1)


        left_process = el.task_parameters_obj.body_of_task.process_that_selected_this_content
        right_process = el.task_parameters_obj.context.process_that_selected_this_content

        recurse_down(session,rewrite_process,left_process,first_pair,second_pair)
        recurse_down(session,rewrite_process,right_process,first_pair,second_pair)



    recurse_down(session,None,root,abstract_pair,remap_pair)

    # for basic_process in to_basic_element_process:
      #  basic_process =Process_Rewrite


    '''
    
    Ver31_rewrite_analogous_idea_prompt = "The text below describes a synoposis of a speech. For each sentence, describe at a high level what " \
                                          "each sentence is doing/serving. For instance, these are examples of higher level 'making a claim to grab listener', 'giving an example to emphasize a point', 'reiteration of a previous statement" \
                                          " with more emotion'," \
                                          " 'follow up on what was said earlier', 'elaboration of idea to clarify claim', 'personal self disclosure to connect to listener','seguing to new idea' "

    Ver31_rewrite_analogous_idea_rate = "Rate how well you feel the high level descriptions capture what is happening on each line of text. "
    rewrite31_idea_pr1 = produce_pairs(Ver31_rewrite_analogous_idea_prompt, Ver31_rewrite_analogous_idea_rate)

    Ver32_convert_prompt = "The text below describes part of speech about racism. Try to rewrite this to incorporate and discuss sexism. Use" \
                           " the roughly same number of sentences and general structure. However, try to change the context and examples to be " \
                           " more appropriate to the topic of sexism. You may use the structure listed in INFO to help frame what is written "
    
    '''

def setup_summary(session):
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    dir_path = os.path.join(dir_path, "backend/little_match_girl")
    little_match_girl=None
    try:
        little_match_girl=open("little_match_girl","rb")
    except:
        little_match_girl = open(dir_path,"rb")
    little_match_girl_text=little_match_girl.read()
    little_match_girl.close()
    little_match_girl=little_match_girl_text

    as_arry=re.split("[.;?]", little_match_girl)
    #as_arry=as_arry[0:len(as_arry)/2]
    match_girl_batch_size_5=[]
    for i in xrange(0,len(as_arry),5):
        match_girl_batch_size_5.append(".".join(as_arry[i:i+5]))

    recurse_summary(session,match_girl_batch_size_5,0,None,match_girl_batch_size_5)



def _merge_step(session,left_content_result,right_content_result,context_result=None):
    default_sub_process_amount = 3
    default_process_amount = 2

    merge_prompt="The text below contains two related parts of a story. Please combine them into a single summary that accounts for the keys points and events in both of them. The context on the left describes what happened before"

    merge_rate="The text below and the left describes two related scenes of a story, please rate how well 'content to be evaluate' incorporates the information into summary that accounts for the key points " \
               "of both of them"

    cr_prompt=Content_Result(merge_prompt,is_completed=True)
    cr_prompt_rate=Content_Result(merge_rate,is_completed=True)



    sub_process = {"prompt": cr_prompt_rate,
                   "expected_results": 1,
                   "context":right_content_result,
                   "content_to_be_requested": default_sub_process_amount}

    merge_process = Process_Merge(body_of_task=left_content_result, context=right_content_result,suggestion=context_result, prompt=cr_prompt,
                                      expected_results=1, content_to_be_requested=default_process_amount,
                                    subprocess_tuple=(Process_Rate,sub_process))

    merge_process.is_using_ml=True

    session.add(merge_process)
    session.commit()
    return merge_process



def _summary_step(session,content,context=None):
    default_sub_process_amount=3
    default_process_amount=2
    summary_prompt="For the text below, to the best to your ability, " \
                   "please write a concise summary that incorporates the keys points and events of the text below. Any text on the left is meant to provide context"

    summary_rate_prompt="The 'content to be evaluated' is intended to be a summary of the text below. " \
                        "Rate how well you feel it accurately captures the full meaning and key events. "

    cr_prompt=Content_Result(summary_prompt,is_completed=True)
    cr_prompt_rate=Content_Result(summary_rate_prompt,is_completed=True)

    body_content = None
    if type(content) == type(""):
        body_content=Content_Result(content,is_completed=True)
    else:
        body_content=content

    if type("") == type(context):
        context=Content_Result(context,is_completed=True)

    sub_process = {"prompt": cr_prompt_rate,
                        "expected_results": 1,
                        "content_to_be_requested": default_sub_process_amount}

    summary_process=Process_Rewrite(body_of_task=body_content,prompt=cr_prompt,
                                    expected_results=1,context=context,content_to_be_requested=default_process_amount,
                                    subprocess_tuple=(Process_Rate, sub_process))
    summary_process.is_using_ml=True

    session.add(summary_process)
    session.commit()
    return summary_process


def recurse_summary(session,text_block_ary, depth,left_adjacent_process=None,entire_text_ary=[]): #So I can get the left node
   # print len(text_block_ary)
    sub_group_len=len(text_block_ary)/2

    if sub_group_len==0:

        relevant_text_block=text_block_ary[0]

        index=entire_text_ary.index(relevant_text_block)
        left_text_element=None

        if index > 0:
            left_text_element=entire_text_ary[index-1]
        return _summary_step(session,text_block_ary[0],left_text_element)


    left= text_block_ary[:sub_group_len]
    right= text_block_ary[sub_group_len:]

    left_process=recurse_summary(session,left,depth+1,left_adjacent_process,entire_text_ary)
    right_process=recurse_summary(session,right,depth+1,left_process,entire_text_ary)

    left_adjacent_results=None
    if left_adjacent_process!=None:

        left_adjacent_results=left_adjacent_process.get_final_results()[0]
    merge_process=_merge_step(session,left_process.get_final_results()[0],right_process.get_final_results()[0],context_result=left_adjacent_results)
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


def setup_narrative_plot(session, text="Two men stand above a grave"):

    default_rewrite_amount = 3
    default_sub_process_amount = 2

    root_body="Two men stand above a grave."
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
        "content_to_be_requested": 1,
        "expected_results": 1
    }

   # third = Process_Text_Manipulation(second.get_final_results()[0], prompt_suggestion, context=None, suggestion=suggestions,
    #                                  expected_results=1,
     #                                 content_to_be_requested=1,
     #                                 subprocess_tuple=(Process_Rate, sub_process_suggestion_info))
    session.add(first)
    session.add(second)
    #session.add(third)

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

    #question_answer_profile_generation(session )
    date_plan(session)
    session.commit()
