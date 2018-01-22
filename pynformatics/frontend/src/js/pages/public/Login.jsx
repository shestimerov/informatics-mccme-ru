import React from "react";

import {Icon, Menu} from "antd";

import style from '../../../css/pages/public/login.css';

import Button from '../../components/utility/Button';
import Input, {InputGroup} from "../../components/utility/Input";
import Checkbox from "../../components/utility/Checkbox";
import Telegram from "../../components/Sidebar/Telegram";

import MainContentWrapper from '../../components/utility/MainContentWrapper';

import {
  Col,
  Row,
} from '../../components/utility/Grid';
import {NavLink, Route} from "react-router-dom";

const FormWrapper = ({title, subtitle, errorMessage, children}) => (
  <div className={style.form}>
    <div className={style.formTitle}>{ title }</div>
    <div className={style.formSubtitle}>{ subtitle }</div>
    <div className={style.errorMessage}><span><Icon type="exclamation-circle-o"/></span>{ errorMessage }</div>
    { children }
  </div>
);

const Login = () => (
  <FormWrapper title="Вход" errorMessage="Сообщение об ошибке если есть">
    <Input
        size="large"
        placeholder="Логин"
      />
      <Input
        size="large"
        placeholder="Пароль"
        type="password"
      />
      <InputGroup className={style.inputGroup}>
        <Button type="primary" className={style.loginButton}>Войти</Button>
        <Checkbox>Запомнить меня</Checkbox>
      </InputGroup>
      <Row>
        <Col span={"24"} className={style.inputGroup}>
          <Button className={style.VKButton}>Войти через ВКонтакте</Button>
          <Button className={style.GmailButton}>Войти через Gmail</Button>
        </Col>
      </Row>
  </FormWrapper>
);

const RegisterAsStudent = () => (
  <FormWrapper
    title="Привет, ученик!"
    subtitle="Ученик может решать задачи, принимать участие в курсах, олимпиадах и сборах, видеть задачи недоступные для гостей"
    errorMessage="Сообщение об ошибке если есть"
  >
    <Input size="large" placeholder="Логин"/>
    <InputGroup className={style.inputGroup}>
      <Col span={16}>
        <Input
          size="large"
          placeholder="Пароль"
          type="password"
        />
      </Col>
      <Col span={8}>
        <Button className={style.generateButton}>Сгенерировать</Button>
      </Col>
    </InputGroup>
    <br/>
    <Input size="large" placeholder="Фамилия"/>
    <Input size="large" placeholder="Имя"/>
    <InputGroup>
      <Col span={12}><Input size="large" placeholder="Город"/></Col>
      <Col span={12}><Input size="large" placeholder="Страна"/></Col>
    </InputGroup>
    <Input size="large" placeholder="E-mail"/>
    <Input size="large" placeholder="Учебное заведение"/>
    <Button type="primary">Зарегестрироваться</Button>
  </FormWrapper>
);

const RegisterAsTeacher = () => (
  <FormWrapper title="Вход3" errorMessage="Сообщение об ошибке если есть">
    <Input
        size="small"
        placeholder="Логин"
      />
      <Input
        size="large"
        placeholder="Пароль"
        type="password"
      />
      <InputGroup className={style.inputGroup}>
        <Button type="primary">Войти</Button>
        <Checkbox>Запомнить меня</Checkbox>
      </InputGroup>
      <Row>
        <Col span={"24"} className={style.socialButtonGroup}>
          <Button className={style.VKButton}>Войти через ВКонтакте</Button>
          <Button className={style.GmailButton}>Войти через Gmail</Button>
        </Col>
      </Row>
  </FormWrapper>
);

const RegisterAsTeam = () => (
  <FormWrapper title="Вход4" errorMessage="Сообщение об ошибке если есть">
    <Input
        size="small"
        placeholder="Логин"
      />
      <Input
        size="large"
        placeholder="Пароль"
        type="password"
      />
      <InputGroup className={style.inputGroup}>
        <Button type="primary">Войти</Button>
        <Checkbox>Запомнить меня</Checkbox>
      </InputGroup>
      <Row>
        <Col span={"24"} className={style.socialButtonGroup}>
          <Button className={style.VKButton}>Войти через ВКонтакте</Button>
          <Button className={style.GmailButton}>Войти через Gmail</Button>
        </Col>
      </Row>
  </FormWrapper>
);

const ResetPassword = () => (
  <FormWrapper title="Вход5" errorMessage="Сообщение об ошибке если есть">
    <Input
        size="small"
        placeholder="Логин"
      />
      <Input
        size="large"
        placeholder="Пароль"
        type="password"
      />
      <InputGroup className={style.inputGroup}>
        <Button type="primary">Войти</Button>
        <Checkbox>Запомнить меня</Checkbox>
      </InputGroup>
      <Row>
        <Col span={"24"} className={style.socialButtonGroup}>
          <Button className={style.VKButton}>Войти через ВКонтакте</Button>
          <Button className={style.GmailButton}>Войти через Gmail</Button>
        </Col>
      </Row>
  </FormWrapper>
);


export default class LoginPage extends React.Component {
  render() {
    const { match } = this.props;

    const options = [
      {url: `${match.url}`, linkText: "Вход", component: Login},
      {url: `${match.url}/register_as_student`, linkText: "Регистрация как ученик", component: RegisterAsStudent},
      {url: `${match.url}/register_as_teacher`, linkText: "Регистрация как учитель", component: RegisterAsTeacher},
      {url: `${match.url}/register_as_team`, linkText: "Регистрация команды", component: RegisterAsTeam},
      {url: `${match.url}/reset_password`, linkText: "Восстановление пароля", component: ResetPassword},
    ];

    const menuItems = options.map(option => (
      <Menu.Item key={option.url}>
        <NavLink
          exact to={option.url}
          className={style.link}
          activeClassName={style.linkActive}
        >
          {option.linkText}
        </NavLink>
      </Menu.Item>
    ));

    const routes = options.map(option => (
      <Route exact path={option.url} component={option.component} key={option.url}/>
    ));

    return (
      <MainContentWrapper>
        <Row type="flex" justify="center">
          <Col xs={22} md={20} style={{marginBottom: "16px"}}>
            <Row type="flex" className={style.wrapper}>
              <Col xs={{span: 22, offset: 1, order: 2}} md={{span: 8, offset: 1, order: 1}}>
                <div className={style.leftColumn}>
                  <Menu className={style.menu}>
                    {menuItems}
                  </Menu>
                  <Telegram/>
                </div>
              </Col>
              <Col xs={{span: 22, offset: 1, order: 1}} md={{span: 13, offset: 1, order: 2}}>
                {routes}
              </Col>
            </Row>
          </Col>
        </Row>
      </MainContentWrapper>
    )
  }
}