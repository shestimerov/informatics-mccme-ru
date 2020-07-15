import io
import os
import traceback
import xmlrpc.client

import requests
import transaction
from pyramid.view import view_config

from pynformatics.contest.ejudge.ejudge_proxy import submit
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.model import SimpleUser, EjudgeProblem, Problem
from pynformatics.models import DBSession
from pynformatics.utils.proxied_request_helpers import peek_request_args
from pynformatics.view.utils import *
from pynformatics.view.utils import is_authorized_id


def checkCapability(request):
    if (not RequestCheckUserCapability(request, 'moodle/ejudge_contests:reload')):
        raise Exception("Auth Error")

def setShowLimits(problem_id, show_limits):
    problem = DBSession.query(Problem).filter(Problem.id == problem_id).first()

    problem.show_limits = show_limits
    with transaction.manager:
        DBSession.merge(problem)
    return "Ok"


@view_config(route_name='problem.limits.show', renderer='string')
def problem_show_limits(request):
    try:
        checkCapability(request)
        return setShowLimits(request.matchdict['problem_id'], 1)
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.submit', renderer='json')
def problem_submits(request):
    # TODO: Refactor it
    user_id = RequestGetUserId(request)
    lang_id = request.params["lang_id"]
    problem_id = request.matchdict["problem_id"]
    statement_id = request.matchdict.get('statement_id')
    input_file = request.POST['file'].file

    try:
        input_file.seek(0)
        _data = {
            'lang_id': lang_id,
            'user_id': user_id,
            'statement_id': statement_id,
        }
        url = 'http://localhost:12346/problem/trusted/{}/submit_v2'.format(problem_id)
        _resp = requests.post(url, files={'file': input_file}, data=_data)
        print('Response from :12346', _resp)
        return _resp.json()
    except Exception as e:
        print(e)
        return {
            "result": "error",
            "message": e.__str__(),
            "stack": traceback.format_exc()
        }


@view_config(route_name='problem.ant.submit', renderer='json')
def problem_ant_submits(request):
    user_id = RequestGetUserId(request)
    user = DBSession.query(SimpleUser).filter(SimpleUser.id == user_id).first()
    lang_id = 67
    run_id1 = request.params["run_id1"]
    run_id2 = request.params["run_id2"]
    run_id3 = request.params["run_id3"]
    run_id4 = request.params["run_id4"]
    map_index = 0
    try:
        map_index = request.params["map_index"]
    except:
        pass
    json_names = request.params["json_names"]
    problem_id = request.matchdict["problem_id"]
    problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == problem_id).first()
    #input_file = request.POST['file'].file
    #filename = request.POST['file'].filename
    filename = "input_file.txt"
    input_file = io.StringIO("{4}${5}\n{0}\n{1}\n{2}\n{3}".format(run_id1, run_id2, run_id3, run_id4, json_names, map_index))
    ejudge_url = request.registry.settings['ejudge.new_client_url']
    return {'res' : submit(input_file, problem.ejudge_contest_id, problem.problem_id, lang_id, user.login, user.password, filename, ejudge_url, user_id)}
    

@view_config(route_name='problem.tests.set_preliminary', renderer='json')
def problem_set_preliminary(request):
    try:
        checkCapability(request)
        problem = DBSession.query(Problem).filter(Problem.id == request.matchdict['problem_id']).first()

        problem.sample_tests = request.params['sample_tests']
        with transaction.manager:
           DBSession.merge(problem)
        return {"result" : "ok", "content" : problem.sample_tests}
    except Exception as e:
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.generate_samples', renderer='json')
def problem_generate_samples(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        problem.generateSamples()
#        res = ""
#        if problem.sample_tests != '':
#            res = "<div class='problem-statement'><div class='sample-tests'><div class='section-title'>Примеры</div>"
#        
#            for i in problem.sample_tests.split(","):
#                res += "<div class='sample-test'>"
#                res += "<div class='input'><div class='title'>Входные данные</div><pre class='content'>"
#                res += get_test(problem, i)
#                res += "</pre></div><div class='output'><div class='title'>Выходные данные</div><pre class='content'>"
#                res += get_corr(problem, i)
#                res += "</pre></div></div>"
#        
#            res += "</div></div>"
#
#        problem.sample_tests_html = res
        with transaction.manager:
           DBSession.merge(problem)
        return {"result" : "ok", "content" : problem.sample_tests}
    except Exception as e:
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.limits.hide', renderer='string')
def problem_hide_limits(request):
    try:
        checkCapability(request)
        return setShowLimits(request.matchdict['problem_id'], 0)
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

@view_config(route_name='problem.tests.count', renderer='string')
def problem_get_tests_count(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
        prob = conf.getProblem(problem.problem_id)
        cnt = 0
        res = ""
        while True:
            cnt += 1
            test_file_name = (prob.tests_dir + prob.test_pat) % cnt
            if os.path.exists(test_file_name):
                res += test_file_name
            else:
                break
        return cnt - 1
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

#def get_test(problem, test_num):
#    conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
#    prob = conf.getProblem(problem.problem_id)
#
#    test_file_name = (prob.tests_dir + prob.test_pat) % int(test_num)
#    if os.path.exists(test_file_name):
#        f = open(test_file_name)
#        res = f.read(255)
#    else:
#        res = test_file_name
#    return res

#def get_corr(problem, test_num):
#    conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
#    prob = conf.getProblem(problem.problem_id)
#
#    corr_file_name = (prob.tests_dir + prob.corr_pat) % int(test_num)
#    if os.path.exists(corr_file_name):
#        f = open(corr_file_name)
#        res = f.read(255)
#    else:
#        res = corr_file_name
#    return res


@view_config(route_name='problem.tests.get_test', renderer='json')
def problem_get_test(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()

        test_num = request.matchdict['test_num']
        return {"num" : int(test_num), "content" : problem.get_test(test_num)}
    except Exception as e:
        return {"result" : "error", "num" : int(request.matchdict['test_num']), "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.tests.add', renderer='json')
def problem_add_test(request):
    try:
        checkCapability(request)
        s = xmlrpc.client.ServerProxy('http://localhost:7080/')

        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
        prob = conf.getProblem(problem.problem_id)

        cnt = 0
        flag = False
        while True:
            cnt += 1
            test_file_name = (prob.tests_dir + prob.test_pat) % cnt
            corr_file_name = (prob.tests_dir + prob.corr_pat) % cnt
            if not os.path.exists(test_file_name):
                flag = True
                break

        if flag:
            s.add_file(test_file_name, request.params['input_data'])
            s.add_file(corr_file_name, request.params['output_data'])
        return {"result" : "ok", "content" : test_file_name}
    except Exception as e:
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.tests.get_corr', renderer='json')
def problem_get_corr(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()

        test_num = request.matchdict['test_num']
        return {"num" : int(test_num), "content" : problem.get_corr(test_num)}
    except Exception as e:
        return {"result" : "error", "num" : int(request.matchdict['test_num']), "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.filter_runs', renderer='json')
def problem_runs_filter_proxy(request):
    user_id = RequestGetUserId(request)  # Returns -1 if not authorised

    if not is_authorized_id(user_id):
        return {'result': 'error', 'message': 'Not authorized'}

    problem_id = request.matchdict.get('problem_id')
    if problem_id is None:
        return {"result": "error", "message": 'Problem id required'}

    filter_params = ['user_id', 'group_id',
                     'lang_id', 'status_id', 'statement_id',
                     'count', 'page',
                     'from_timestamp', 'to_timestamp']

    params, _ = peek_request_args(request, filter_params)

    try:
        checkCapability(request)
        params['show_hidden'] = True
        if request.params.get('include_source'):
            params['include_source'] = True
    except Exception as exc:
        pass

    try:
        resp = requests.get('http://localhost:12346/problem/{}/submissions/'.format(problem_id), params=params)
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        print('Request to :12346 failed!')
        print(str(e))
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}


@view_config(route_name='problem.runs.source', renderer='json')
def problem_get_run_source(request):
    run_id = request.matchdict.get('run_id')
    if run_id is None:
        return {"result": "error", "message": 'Run id required'}

    user_id = RequestGetUserId(request)

    if not is_authorized_id(user_id):
        return {'result': 'error', 'message': 'Not authorized'}

    is_admin = RequestCheckUserCapability(request, 'moodle/ejudge_submits:comment')

    params = {
        'is_admin': is_admin,
        'user_id': user_id,
    }

    try:
        url = 'http://localhost:12346/problem/run/{}/source/'.format(run_id)
        resp = requests.get(url, params=params)
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        print('Request to :12346 failed!')
        print(str(e))
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}
