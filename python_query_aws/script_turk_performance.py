from python_query_aws import script_current_task_results
from sqlalchemy import desc
from backend import db_connection2 as db




def formatted_content(element, mturk_submission_time, offset):
    '''
    Shows the element, date, and relative date in comparison to when submitted
    :param element:
    :param offset:
    :return:
    '''
    currentTimeTaskFinished = element.completed_date.replace(tzinfo=mturk_submission_time.tzinfo)

    time_diff = currentTimeTaskFinished - mturk_submission_time

    time_since_work_done = offset - time_diff.total_seconds()

    str_result, str_time, str_absolute_time = str(element.results), str(time_since_work_done), str(
        currentTimeTaskFinished)

    return {"result": str_result, "absolute_time": str_absolute_time, "relative_time": str_time}


def get_recently_submitted_results(session,current_turk_results,max_results=3,time_offset=14395.592572):
    '''
    gets recent user results that are in db and mturk - linkage from the two
    :param session: db object
    :param current_turk_results: turk json
    :param max_results: max per user
    :param time_offset: default amount of time offset between mturk and db 14395.592572
    :return:
    '''
    results=current_turk_results

    enum_assignments = script_current_task_results.task_result_parameters.Assignments


    user_list = []

    for user_data in results[enum_assignments.value]: #get relevant user info
        user_turk_task_info = user_data
        user_exists, user_quality = False, "unknown"

        enum_workerID = script_current_task_results.task_result_parameters.Worker_ID.value
        enum_completedTime = script_current_task_results.task_result_parameters.SubmitTime.value
        enum_assignmentID=script_current_task_results.task_result_parameters.Assignment_ID.value


        user = user_turk_task_info[enum_workerID]
        completion_time = user_turk_task_info[enum_completedTime]
        assignmentID=user_turk_task_info[enum_assignmentID]


        json_results = {"user": user, "user_exists": user_exists, "user_quality": user_quality, "results": [],
                        "latest_turk_submission_time": str(completion_time),"assignment_id":assignmentID}

        user_info = session.query(db.User).filter(db.User.name == user).all()

        if len(user_info) > 0: user_exists = True
        if user_exists:
            user_quality = user_info[0].alias
            json_results["user_quality"] = user_quality
            json_results["user_exists"] = user_exists

            result = session.query(db.Content).filter(db.Content.user_id == user).order_by(
                desc(db.Content.completed_date)).limit(max_results).all()

            # get user results sorted
            # get most recent - compare date to latest mturk submission date - measure offset :(
            # If offset greater than X, those lying mother fuckers, else approve

            for element in result:
                vals = formatted_content(element, completion_time, time_offset)

                json_results["results"].append(vals)

            user_list.append(json_results)

    return user_list


if __name__ == '__main__':


    db_name="Task_Crowd_Source_Test"

    conn, meta, session = db.connect("postgres", "1234", db=db_name)

    results=script_current_task_results.get_active_users_in_latest_task(0,"live")

    print get_recently_submitted_results(session,results,max_results=2,time_offset=14395.592572 )

